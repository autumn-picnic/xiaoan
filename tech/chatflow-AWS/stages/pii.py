"""PII redaction: tag [NAME] [PHONE] [ADDRESS] [ID_NUMBER] before any external call."""
import re

_PATTERNS = [
    (re.compile(r"1[3-9]\d{9}"), "[PHONE]"),
    (re.compile(r"\d{15}|\d{17}[\dXx]"), "[ID_NUMBER]"),
    # Street-level address pattern (中文地址)
    (re.compile(r"[一-龥]{2,5}(省|市|区|县|街|路|号|村|镇|乡)[一-龥\d]{1,20}"), "[ADDRESS]"),
]


def run(state: dict) -> dict:
    text = state["user_input"]
    for pattern, tag in _PATTERNS:
        text = pattern.sub(tag, text)
    return {**state, "redacted_input": text}
