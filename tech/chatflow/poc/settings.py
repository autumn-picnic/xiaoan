from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any


DEFAULT_MODEL = "gpt-4o-mini"
CONFIG_PATH = Path(
    os.getenv("XIAOAN_CONFIG_PATH", str(Path.home() / ".config" / "xiaoan-chatflow" / "config.json"))
)


class SettingsError(ValueError):
    pass


def load_config() -> dict[str, Any]:
    if not CONFIG_PATH.exists():
        return {}
    try:
        return json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SettingsError(f"invalid config JSON: {CONFIG_PATH}") from exc


def save_config(*, model: str | None = None, api_key: str | None = None) -> Path:
    config = load_config()
    if model is not None:
        config["model"] = model
    if api_key is not None:
        config["api_key"] = api_key
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    CONFIG_PATH.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    CONFIG_PATH.chmod(0o600)
    return CONFIG_PATH


def clear_config() -> None:
    if CONFIG_PATH.exists():
        CONFIG_PATH.unlink()


def get_model(cli_model: str | None = None) -> str:
    if cli_model:
        return cli_model
    if os.getenv("XIAOAN_MODEL"):
        return os.environ["XIAOAN_MODEL"]
    return str(load_config().get("model") or DEFAULT_MODEL)


def get_api_key() -> str:
    if os.getenv("OPENAI_API_KEY"):
        return os.environ["OPENAI_API_KEY"]
    return str(load_config().get("api_key") or "")


def masked_api_key() -> str:
    api_key = get_api_key()
    if not api_key:
        return ""
    if len(api_key) <= 10:
        return "***"
    return f"{api_key[:5]}...{api_key[-4:]}"
