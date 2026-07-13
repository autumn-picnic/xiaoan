"""Safety scan: detect hard red flags → Crisis SOP.

Conservative threshold per architecture.md: only hard signals trigger crisis.
Ambiguous signals ("I'm scared") stay in normal flow.
"""

# Hard red-flag phrases (violence in progress, weapons, child danger, self-harm)
_RED_FLAGS = [
    "打我", "打死", "杀", "刀", "枪", "伤", "血", "不能打电话",
    "监控手机", "跟踪", "孩子", "儿子", "女儿", "自杀", "轻生", "死了算了",
    "不让我出门", "锁门",
]


def run(state: dict) -> dict:
    text = state.get("redacted_input", state["user_input"]).lower()
    red_flag = any(kw in text for kw in _RED_FLAGS)
    return {**state, "red_flag": red_flag}
