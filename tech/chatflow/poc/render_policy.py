from __future__ import annotations

from typing import Any


DEFAULT_GROUND_TRIGGER_TERMS = [
    "法律依据",
    "法律规定",
    "法条",
    "依据",
    "条件",
    "证据",
    "材料",
    "流程",
    "怎么申请",
    "怎么报警",
    "怎么办理",
    "时限",
    "多久",
    "费用",
    "免费",
    "后果",
    "管辖",
    "法院",
    "有效期",
    "违反",
    "能不能",
    "可以吗",
    "算不算",
]


def get_render_policy(capsule: dict[str, Any]) -> dict[str, Any]:
    policy = capsule.get("render_policy")
    return policy if isinstance(policy, dict) else {}


def ground_policy(capsule: dict[str, Any]) -> str:
    raw_policy = str(get_render_policy(capsule).get("ground", "on_demand")).strip()
    return raw_policy or "on_demand"


def ground_trigger_terms(capsule: dict[str, Any]) -> list[str]:
    raw_terms = get_render_policy(capsule).get("ground_triggers", [])
    custom_terms = [str(term).strip() for term in raw_terms if str(term).strip()] if isinstance(raw_terms, list) else []
    return custom_terms + DEFAULT_GROUND_TRIGGER_TERMS


def has_ground_intent(message: str, capsule: dict[str, Any]) -> bool:
    return any(term in message for term in ground_trigger_terms(capsule))


def should_load_ground(
    capsule: dict[str, Any],
    message: str,
    *,
    already_loaded: bool = False,
) -> tuple[bool, str]:
    policy = ground_policy(capsule)
    if policy in {"always", "on_entry"}:
        return True, f"render_policy.ground={policy}"
    if policy == "never":
        return False, "render_policy.ground=never"
    if already_loaded:
        return True, "ground already loaded for active capsule"
    if has_ground_intent(message, capsule):
        return True, "message matched ground intent trigger"
    return False, "render_policy.ground=on_demand and no ground intent"


def capsule_for_render(capsule: dict[str, Any], *, include_ground: bool) -> dict[str, Any]:
    if include_ground:
        return capsule
    rendered = dict(capsule)
    rendered["ground"] = {}
    return rendered
