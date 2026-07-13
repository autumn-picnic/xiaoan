from __future__ import annotations

from dataclasses import dataclass


IMMEDIATE_DANGER_TERMS = [
    "正在打",
    "现在打",
    "刚刚打",
    "拿刀",
    "持刀",
    "要杀",
    "杀了我",
    "堵门",
    "砸门",
    "冲进来",
    "不让我走",
    "被关起来",
]

SELF_HARM_TERMS = [
    "不想活",
    "活不下去",
    "想死",
    "自杀",
    "伤害自己",
]


@dataclass
class SafetySignal:
    level: str
    reason: str
    message: str

    @property
    def is_red_flag(self) -> bool:
        return self.level in {"immediate_danger", "self_harm"}


def scan_safety(user_message: str) -> SafetySignal:
    if any(term in user_message for term in SELF_HARM_TERMS):
        return SafetySignal(
            level="self_harm",
            reason="user message contains self-harm language",
            message="如果你现在有伤害自己的冲动,请优先联系身边可信的人、当地紧急电话或危机干预热线;先不要独自承受。",
        )
    if any(term in user_message for term in IMMEDIATE_DANGER_TERMS):
        return SafetySignal(
            level="immediate_danger",
            reason="user message suggests immediate physical danger",
            message="如果你现在正处于危险现场,请优先离开危险位置并拨打 110;能联系可信亲友或邻居时,先让现实中的人介入保护你。",
        )
    return SafetySignal(level="normal", reason="", message="")
