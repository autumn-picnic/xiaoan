from __future__ import annotations


def is_unsupported_temperature_error(exc: Exception) -> bool:
    message = str(exc).lower()
    return "temperature" in message and (
        "unsupported" in message or "does not support" in message or "only the default" in message
    )
