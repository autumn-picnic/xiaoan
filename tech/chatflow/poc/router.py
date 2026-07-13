from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from openai_compat import is_unsupported_temperature_error
from settings import DEFAULT_MODEL, get_api_key, get_model

REPO_ROOT = Path(__file__).resolve().parents[3]
CAPSULES_JSON = Path(__file__).resolve().parent / "capsules.json"
BASELINE_CAPSULE_ID = "baseline"
BASELINE_MESSAGES = {
    "你好",
    "您好",
    "hello",
    "hi",
    "hey",
    "在吗",
    "谢谢",
    "谢谢你",
    "好的",
    "嗯",
    "ok",
}
PHYSICAL_VIOLENCE_TERMS = [
    "打我",
    "打了我",
    "又打",
    "被打",
    "动手",
    "揍我",
    "扇我",
    "殴打",
    "家暴",
]
EXPLICIT_INTENT_KEYWORDS = {
    "n3a": ["报警", "警察", "派出所", "回执", "出警", "告诫书"],
    "n2a": ["证据", "留证", "录音", "录像", "截图", "聊天记录", "就医记录"],
    "n5p": ["保护令", "法院", "禁止靠近", "不让他靠近", "远离我", "不能接近"],
    "n5d": ["离婚", "要不要离", "该不该离"],
    "k1": [
        "我也有错",
        "惹他生气",
        "是不是我",
        "不算家暴",
        "为了我好",
        "算不算家暴",
        "是不是家暴",
        "是家暴吗",
        "这正常吗",
        "正常的吗",
        "正常吗",
        "他这样可以吗",
        "这样打",
        "我有错吗",
    ],
}
DISCLOSURE_FOLLOWUP_INTENT_TERMS = [
    "?",
    "？",
    "吗",
    "怎么办",
    "怎么做",
    "怎么处理",
    "要怎么办",
    "我不知道怎么办",
    "能不能",
    "可以吗",
    "是不是",
    "算不算",
    "正常吗",
    "这正常吗",
    "正常的吗",
    "对吗",
    "为什么",
    "该不该",
    "要不要",
    "有没有",
    "我也有错",
    "我有错吗",
    "他这样可以吗",
]
HEURISTIC_BOOSTS = {
    "n3a": ["报警", "警察", "派出所", "回执", "出警", "告诫书", "笔录", "拿刀", "持刀", "不敢出去"],
    "n2a": ["证据", "留证", "录音", "录像", "截图", "聊天记录", "就医记录"],
    "n5p": ["保护令", "禁止", "靠近", "法院", "远离我", "不能接近"],
    "n6a": ["分居后", "离婚了", "前夫", "前男友", "跟踪", "骚扰", "堵我", "打电话骂"],
    "n5d": ["要不要离婚", "是否离婚", "离不离婚", "怕离了", "该不该离"],
    "k1": [
        "不算家暴",
        "算不算家暴",
        "是不是家暴",
        "是家暴吗",
        "我也有错",
        "我有错吗",
        "惹他生气",
        "为了我好",
        "冷暴力",
        "正常吗",
        "这正常吗",
        "正常的吗",
        "他这样可以吗",
        "这样打",
    ],
}


@dataclass
class RouteDecision:
    capsule_id: str
    confidence: float
    reason: str
    should_continue_active_capsule: bool = False
    method: str = "llm"

    def to_json(self) -> dict[str, Any]:
        return {
            "capsule_id": self.capsule_id,
            "confidence": self.confidence,
            "reason": self.reason,
            "should_continue_active_capsule": self.should_continue_active_capsule,
            "method": self.method,
        }


class RouterError(ValueError):
    pass


class CapsuleRouter(Protocol):
    def route(
        self,
        message: str,
        capsules: list[dict[str, Any]],
        *,
        active_capsule_id: str = "",
        conversation_context: list[dict[str, str]] | None = None,
    ) -> RouteDecision:
        pass


class LLMRouter:
    def __init__(self, model: str | None = None) -> None:
        self.model = model

    def route(
        self,
        message: str,
        capsules: list[dict[str, Any]],
        *,
        active_capsule_id: str = "",
        conversation_context: list[dict[str, str]] | None = None,
    ) -> RouteDecision:
        rule_decision = route_with_baseline_rules(message)
        if rule_decision:
            return rule_decision
        return route_with_llm(message, capsules, active_capsule_id, self.model, conversation_context)


class HeuristicTestRouter:
    def route(
        self,
        message: str,
        capsules: list[dict[str, Any]],
        *,
        active_capsule_id: str = "",
        conversation_context: list[dict[str, str]] | None = None,
    ) -> RouteDecision:
        return route_with_heuristic(message, capsules, active_capsule_id)


def select_router(*, offline: bool, model: str | None = None) -> CapsuleRouter:
    return HeuristicTestRouter() if offline else LLMRouter(model)


def load_capsules() -> list[dict[str, Any]]:
    if not CAPSULES_JSON.exists():
        raise RouterError("capsules.json not found; run capsule_loader.py first")
    return json.loads(CAPSULES_JSON.read_text(encoding="utf-8"))


def compact_capsule_card(capsule: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": capsule["id"],
        "title": capsule["title"],
        "triggers": capsule.get("triggers", [])[:12],
        "use_when": capsule.get("use_when", [])[:8],
        "do_not_use_when": capsule.get("do_not_use_when", [])[:8],
        "has_ground": bool(
            capsule.get("ground", {}).get("summary")
            or capsule.get("ground", {}).get("legal_basis")
            or capsule.get("ground", {}).get("practice_basis")
            or capsule.get("ground", {}).get("nodes")
        ),
        "issue_count": len(capsule.get("issues", [])),
    }


def router_prompt(
    message: str,
    capsules: list[dict[str, Any]],
    active_capsule_id: str = "",
    conversation_context: list[dict[str, str]] | None = None,
) -> list[dict[str, str]]:
    cards = [compact_capsule_card(capsule) for capsule in capsules]
    system = (
        "你是小安 POC 的胶囊路由器。你的任务是从候选胶囊中选择最适合回答用户当前问题的 capsule_id。"
        "先用 triggers 召回,再用 use_when 精筛,最后用 do_not_use_when 排除。"
        "如果用户明显延续上一轮 active capsule 的同一任务,可以继续 active capsule。"
        "如果当前消息本身很短或含糊,必须结合 conversation_context 判断是否是上一轮的追问。"
        "如果用户只是问候、寒暄、感谢、测试系统、或没有表达具体家暴/法律/求助意图,"
        "必须返回 capsule_id=\"baseline\",不要为了匹配而强行选择某个胶囊。"
        "例如用户只说“你好”时,返回 baseline,不要匹配 n3。"
        "如果用户只是纯披露被打/被家暴,且没有任何问题、判断、定义困惑或求助意图,"
        "才返回 capsule_id=\"baseline\",由主 agent 自然承接。"
        "如果用户问“算不算家暴”“是不是家暴”“这正常吗”“我也有错吗”“他这样可以吗”等识别困惑,"
        "不要被 baseline 截断,应选择最贴近的识别/认知类胶囊。"
        "只输出 JSON,不要输出额外文字。JSON 字段必须是: "
        "capsule_id, confidence, reason, should_continue_active_capsule。"
        "confidence 是 0 到 1 的数字。"
    )
    user = {
        "user_message": message,
        "active_capsule_id": active_capsule_id,
        "conversation_context": conversation_context or [],
        "fallback_capsule_id": BASELINE_CAPSULE_ID,
        "capsules": cards,
    }
    return [
        {"role": "system", "content": system},
        {"role": "user", "content": json.dumps(user, ensure_ascii=False)},
    ]


def parse_llm_json(content: str) -> dict[str, Any]:
    content = content.strip()
    if content.startswith("```"):
        content = re.sub(r"^```(?:json)?\s*", "", content)
        content = re.sub(r"\s*```$", "", content)
    return json.loads(content)


def route_with_llm(
    message: str,
    capsules: list[dict[str, Any]],
    active_capsule_id: str = "",
    model: str | None = None,
    conversation_context: list[dict[str, str]] | None = None,
) -> RouteDecision:
    api_key = get_api_key()
    if not api_key:
        raise RouterError("OPENAI_API_KEY is not set; use --offline for heuristic local testing")

    try:
        from openai import BadRequestError, OpenAI
    except ImportError as exc:
        raise RouterError("openai package is not installed; install it or use --offline") from exc

    client = OpenAI(api_key=api_key)
    request_kwargs: dict[str, Any] = {
        "model": get_model(model),
        "messages": router_prompt(message, capsules, active_capsule_id, conversation_context),
        "temperature": 0,
        "response_format": {"type": "json_object"},
    }
    try:
        response = client.chat.completions.create(**request_kwargs)
    except BadRequestError as exc:
        if not is_unsupported_temperature_error(exc):
            raise
        request_kwargs.pop("temperature", None)
        response = client.chat.completions.create(**request_kwargs)
    content = response.choices[0].message.content or "{}"
    payload = parse_llm_json(content)
    return validate_decision(payload, capsules, method="llm")


def tokenize_zh_light(text: str) -> set[str]:
    words = set(re.findall(r"[A-Za-z0-9]+", text.lower()))
    # For Chinese MVP fallback, character bigrams are good enough to smoke-test routing without API calls.
    chinese = "".join(re.findall(r"[\u4e00-\u9fff]+", text))
    words.update(chinese[idx : idx + 2] for idx in range(max(0, len(chinese) - 1)))
    return {word for word in words if word.strip()}


def route_with_heuristic(
    message: str,
    capsules: list[dict[str, Any]],
    active_capsule_id: str = "",
) -> RouteDecision:
    if is_baseline_message(message):
        return RouteDecision(
            capsule_id=BASELINE_CAPSULE_ID,
            confidence=0.99,
            reason="offline heuristic: baseline greeting/no concrete scenario",
            should_continue_active_capsule=False,
            method="heuristic",
        )
    baseline = baseline_for_physical_violence_disclosure(message)
    if baseline:
        return baseline

    message_tokens = tokenize_zh_light(message)
    scored: list[tuple[float, dict[str, Any], str, bool]] = []
    for capsule in capsules:
        haystacks = capsule.get("triggers", []) + capsule.get("use_when", [])
        score = 0.0
        reasons: list[str] = []
        for keyword in HEURISTIC_BOOSTS.get(capsule["id"], []):
            if keyword in message:
                score += 6.0
                reasons.append(f"keyword: {keyword}")
        for text in haystacks:
            if text and text in message:
                score += 8.0
                reasons.append(f"direct phrase: {text[:18]}")
            overlap = len(message_tokens & tokenize_zh_light(text))
            if overlap:
                score += overlap
        if active_capsule_id and capsule["id"] == active_capsule_id:
            score += 1.5
            reasons.append("active capsule continuity")
        has_strong_signal = bool(reasons)
        scored.append((score, capsule, "; ".join(reasons) or "token overlap", has_strong_signal))

    scored.sort(key=lambda item: item[0], reverse=True)
    best_score, best_capsule, reason, has_strong_signal = scored[0]
    if best_score < 3 or (not has_strong_signal and best_score < 14):
        return RouteDecision(
            capsule_id=BASELINE_CAPSULE_ID,
            confidence=0.75,
            reason="offline heuristic: no capsule scored above baseline threshold",
            should_continue_active_capsule=False,
            method="heuristic",
        )
    confidence = min(0.95, max(0.05, best_score / 20.0))
    return RouteDecision(
        capsule_id=best_capsule["id"],
        confidence=round(confidence, 2),
        reason=f"offline heuristic: {reason}",
        should_continue_active_capsule=bool(active_capsule_id and best_capsule["id"] == active_capsule_id),
        method="heuristic",
    )


def validate_decision(payload: dict[str, Any], capsules: list[dict[str, Any]], method: str) -> RouteDecision:
    ids = {capsule["id"] for capsule in capsules}
    capsule_id = str(payload.get("capsule_id", "")).strip().lower()
    if capsule_id in {"", "none", "null", "no_match", "fallback", "default"}:
        capsule_id = BASELINE_CAPSULE_ID
    if capsule_id != BASELINE_CAPSULE_ID and capsule_id not in ids:
        raise RouterError(f"router returned unknown capsule_id: {capsule_id}")
    confidence = float(payload.get("confidence", 0))
    confidence = max(0.0, min(1.0, confidence))
    return RouteDecision(
        capsule_id=capsule_id,
        confidence=confidence,
        reason=str(payload.get("reason", "")).strip(),
        should_continue_active_capsule=bool(payload.get("should_continue_active_capsule", False)),
        method=method,
    )


def route_message(
    message: str,
    capsules: list[dict[str, Any]] | None = None,
    active_capsule_id: str = "",
    model: str | None = None,
    offline: bool = False,
    conversation_context: list[dict[str, str]] | None = None,
) -> RouteDecision:
    capsules = capsules or load_capsules()
    if not capsules:
        raise RouterError("no capsules loaded")
    return select_router(offline=offline, model=model).route(
        message,
        capsules,
        active_capsule_id=active_capsule_id,
        conversation_context=conversation_context,
    )


def route_with_baseline_rules(message: str) -> RouteDecision | None:
    if is_baseline_message(message):
        return RouteDecision(
            capsule_id=BASELINE_CAPSULE_ID,
            confidence=0.99,
            reason="baseline: greeting/no concrete scenario",
            should_continue_active_capsule=False,
            method="rule",
        )
    baseline = baseline_for_physical_violence_disclosure(message)
    if baseline:
        return baseline
    return None


def is_baseline_message(message: str) -> bool:
    normalized = re.sub(r"[\s。！!？?，,~～.]+", "", message.strip().lower())
    if normalized in BASELINE_MESSAGES:
        return True
    # Very short generic text should not be forced into a high-stakes capsule.
    if len(normalized) <= 2 and normalized not in {"打我", "报警"}:
        return True
    return False


def baseline_for_physical_violence_disclosure(message: str) -> RouteDecision | None:
    if not any(term in message for term in PHYSICAL_VIOLENCE_TERMS):
        return None
    if has_disclosure_followup_intent(message):
        return None
    for capsule_id, keywords in EXPLICIT_INTENT_KEYWORDS.items():
        if any(keyword in message for keyword in keywords):
            return None
    return RouteDecision(
        capsule_id=BASELINE_CAPSULE_ID,
        confidence=0.92,
        reason="baseline: physical violence disclosure without concrete action intent",
        should_continue_active_capsule=False,
        method="rule",
    )


def has_disclosure_followup_intent(message: str) -> bool:
    return any(term in message for term in DISCLOSURE_FOLLOWUP_INTENT_TERMS)


def main() -> None:
    parser = argparse.ArgumentParser(description="Route a user message to a XiaoAn capsule.")
    parser.add_argument("message", help="User message to route.")
    parser.add_argument("--active-capsule-id", default="", help="Previous active capsule id, if any.")
    parser.add_argument("--model", default="")
    parser.add_argument("--offline", action="store_true", help="Use deterministic heuristic routing without OpenAI.")
    args = parser.parse_args()

    decision = route_message(
        args.message,
        active_capsule_id=args.active_capsule_id,
        model=args.model,
        offline=args.offline,
    )
    print(json.dumps(decision.to_json(), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
