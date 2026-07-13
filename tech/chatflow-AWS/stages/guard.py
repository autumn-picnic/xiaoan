"""Output guard: block unsafe or off-topic responses before delivery."""

_BLOCKED_PATTERNS = [
    "我是AI", "我是语言模型", "我无法",  # avoid breaking immersion unhelpfully
]


def run(state: dict) -> dict:
    response = state.get("response", "")

    for pattern in _BLOCKED_PATTERNS:
        if pattern in response:
            response = _fallback(state)
            break

    return {**state, "response": response}


def _fallback(state: dict) -> str:
    return (
        "我在这里陪着你。能告诉我更多发生了什么吗？"
        "如有紧急情况请拨打110，或联系全国家暴热线400-779-9995。"
    )
