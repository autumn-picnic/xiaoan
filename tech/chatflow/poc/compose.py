from __future__ import annotations

import json
from typing import Any, Protocol

from ground import GroundItem
from openai_compat import is_unsupported_temperature_error
from settings import get_api_key, get_model


class ComposeError(ValueError):
    pass


class SupportAgent(Protocol):
    def compose(
        self,
        user_message: str,
        capsule: dict[str, Any],
        ground_items: list[GroundItem],
        *,
        safety_message: str = "",
        previous_response_id: str = "",
    ) -> tuple[str, str]:
        pass


class LLMSupportAgent:
    def __init__(self, model: str | None = None) -> None:
        self.model = model

    def compose(
        self,
        user_message: str,
        capsule: dict[str, Any],
        ground_items: list[GroundItem],
        *,
        safety_message: str = "",
        previous_response_id: str = "",
    ) -> tuple[str, str]:
        return compose_with_llm(
            user_message,
            capsule,
            ground_items,
            safety_message=safety_message,
            model=self.model,
            previous_response_id=previous_response_id,
        )


class TemplateTestSupportAgent:
    def compose(
        self,
        user_message: str,
        capsule: dict[str, Any],
        ground_items: list[GroundItem],
        *,
        safety_message: str = "",
        previous_response_id: str = "",
    ) -> tuple[str, str]:
        return render_offline_answer(user_message, capsule, ground_items, safety_message), previous_response_id


def select_support_agent(*, offline: bool, model: str | None = None) -> SupportAgent:
    return TemplateTestSupportAgent() if offline else LLMSupportAgent(model)


def flatten_points(recognize: dict[str, Any], limit: int = 5) -> list[str]:
    points = list(recognize.get("points") or [])
    if points:
        return points[:limit]
    for group in recognize.get("groups") or []:
        points.extend(group.get("points") or [])
    return points[:limit]


def format_ground_for_prompt(ground_items: list[GroundItem]) -> str:
    if not ground_items:
        return "（本轮没有成功解析的法律依据;不要编造法条。）"
    blocks: list[str] = []
    for idx, item in enumerate(ground_items, start=1):
        note = f"\n用途:{item.note}" if item.note else ""
        blocks.append(
            f"[{idx}] {item.title}\nref:{item.ref}\nsource_ref:{item.source_ref}{note}\n原文:{item.text}"
        )
    return "\n\n".join(blocks)


def render_offline_answer(
    user_message: str,
    capsule: dict[str, Any],
    ground_items: list[GroundItem],
    safety_message: str = "",
) -> str:
    lines: list[str] = []
    if safety_message:
        lines.extend([f"先说安全: {safety_message}", ""])

    lines.append(f"我会先按「{capsule['title']}」这条路径帮你梳理。")

    recognize_points = flatten_points(capsule.get("recognize", {}), limit=4)
    if recognize_points:
        lines.extend(["", "你先记住几件事:"])
        lines.extend(f"- {point}" for point in recognize_points)

    steps = capsule.get("act", {}).get("steps") or []
    if steps:
        lines.extend(["", "接下来可以这样做:"])
        for raw_step in steps[:6]:
            if isinstance(raw_step, dict):
                action = raw_step.get("action", "")
                detail = raw_step.get("detail", "")
                lines.append(f"- {action}: {detail}" if detail else f"- {action}")
            else:
                lines.append(f"- {raw_step}")

    ground = capsule.get("ground", {})
    legal_basis = ground.get("legal_basis") or []
    if legal_basis:
        lines.extend(["", "法律依据:"])
        lines.extend(f"- {item}" for item in legal_basis[:5])

    practice_basis = ground.get("practice_basis") or []
    if practice_basis:
        lines.extend(["", "实践/经验依据:"])
        lines.extend(f"- {item}" for item in practice_basis[:5])

    if ground_items:
        lines.extend(["", "已解析依据原文:"])
        for item in ground_items[:5]:
            note = f" — {item.note}" if item.note else ""
            lines.append(f"- {item.title}（{item.source_ref}）{note}")

    limits = ground.get("limits") or []
    if limits:
        lines.extend(["", "边界提醒:"])
        lines.extend(f"- {limit}" for limit in limits[:3])

    return "\n".join(lines)


def build_messages(
    user_message: str,
    capsule: dict[str, Any],
    ground_items: list[GroundItem],
    safety_message: str = "",
) -> list[dict[str, str]]:
    system = (
        "你是小安,一个面向家暴受害者的中文支持型助手。"
        "你要用温和、清晰、可执行的中文回答。"
        "你不能替代律师,不能保证结果,不能编造法律依据。"
        "如果存在即时危险,优先安全和报警。"
        "回答要使用胶囊的 Recognize/Act/Ground 结构,但不要机械输出字段名。"
        "Ground 分为 summary(总体依据说明)、legal_basis(法律依据)、practice_basis(实践/NGO 经验依据);"
        "resolved_ground 包含法律 wiki 节点全文和该节点声明的 source_ref 相关原文片段,优先据此作答;"
        "如果本轮没有提供 ground/resolved_ground,先用 Recognize/Act 承接,不要主动输出具体法律依据;"
        "只能使用提供的依据,不要编造法条、数据或来源。"
    )
    ground = capsule.get("ground", {})
    payload = {
        "user_message": user_message,
        "safety_message": safety_message,
        "capsule": {
            "id": capsule.get("id"),
            "title": capsule.get("title"),
            "recognize": capsule.get("recognize"),
            "act": capsule.get("act"),
            "ground": {
                "summary": ground.get("summary"),
                "legal_basis": ground.get("legal_basis"),
                "practice_basis": ground.get("practice_basis"),
                "limits": ground.get("limits"),
            },
            "safety_note": capsule.get("safety_note"),
            "ai_stance": capsule.get("ai_stance"),
        },
        "resolved_ground": [item.to_json() for item in ground_items],
    }
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
    ]


def build_response_input(
    user_message: str,
    capsule: dict[str, Any],
    ground_items: list[GroundItem],
    safety_message: str = "",
) -> str:
    messages = build_messages(user_message, capsule, ground_items, safety_message)
    return "\n\n".join(f"{message['role'].upper()}:\n{message['content']}" for message in messages)


def compose_with_llm(
    user_message: str,
    capsule: dict[str, Any],
    ground_items: list[GroundItem],
    safety_message: str = "",
    model: str | None = None,
    previous_response_id: str = "",
) -> tuple[str, str]:
    api_key = get_api_key()
    if not api_key:
        raise ComposeError("OPENAI_API_KEY is not set; use --offline for local deterministic rendering")

    try:
        from openai import BadRequestError, OpenAI
    except ImportError as exc:
        raise ComposeError("openai package is not installed; install it or use --offline") from exc

    client = OpenAI(api_key=api_key)
    selected_model = get_model(model)

    if hasattr(client, "responses"):
        kwargs: dict[str, Any] = {
            "model": selected_model,
            "input": build_response_input(user_message, capsule, ground_items, safety_message),
            "temperature": 0.3,
        }
        if previous_response_id:
            kwargs["previous_response_id"] = previous_response_id
        try:
            response = client.responses.create(**kwargs)
        except BadRequestError as exc:
            if not is_unsupported_temperature_error(exc):
                raise
            kwargs.pop("temperature", None)
            response = client.responses.create(**kwargs)
        text = getattr(response, "output_text", "") or ""
        return text, getattr(response, "id", "") or previous_response_id

    request_kwargs: dict[str, Any] = {
        "model": selected_model,
        "messages": build_messages(user_message, capsule, ground_items, safety_message),
        "temperature": 0.3,
    }
    try:
        response = client.chat.completions.create(**request_kwargs)
    except BadRequestError as exc:
        if not is_unsupported_temperature_error(exc):
            raise
        request_kwargs.pop("temperature", None)
        response = client.chat.completions.create(**request_kwargs)
    return response.choices[0].message.content or "", previous_response_id
