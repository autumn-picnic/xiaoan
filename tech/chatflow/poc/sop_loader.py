from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[3]
SOP_DIR = REPO_ROOT / "knowledge" / "sops"
CRISIS_SOP_FILE = SOP_DIR / "crisis-sop.md"
BASELINE_SOP_FILE = SOP_DIR / "main-agent-baseline-sop.md"
DEFAULT_SAFETY_MESSAGE = "如果你现在处于危险中,请优先离开危险位置并拨打 110。"


class SOPLoadError(ValueError):
    pass


def read_sop(path: Path) -> str:
    if not path.exists():
        raise SOPLoadError(f"SOP file not found: {path.relative_to(REPO_ROOT)}")
    return path.read_text(encoding="utf-8")


def parse_sop(path: Path) -> dict[str, Any]:
    text = read_sop(path)
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)$", text, re.DOTALL)
    if not match:
        raise SOPLoadError(f"SOP file missing YAML frontmatter: {path.relative_to(REPO_ROOT)}")
    try:
        data = yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError as exc:
        raise SOPLoadError(f"invalid SOP frontmatter: {path.relative_to(REPO_ROOT)}: {exc}") from exc
    if not isinstance(data, dict):
        raise SOPLoadError(f"SOP frontmatter must be a mapping: {path.relative_to(REPO_ROOT)}")
    if not data.get("id") or not data.get("title"):
        raise SOPLoadError(f"SOP must define id and title: {path.relative_to(REPO_ROOT)}")
    data.setdefault("issues", [])
    data["body"] = match.group(2).strip()
    data["path"] = str(path.relative_to(REPO_ROOT))
    return data


def load_crisis_sop() -> dict[str, Any]:
    return parse_sop(CRISIS_SOP_FILE)


def load_baseline_sop() -> dict[str, Any]:
    return parse_sop(BASELINE_SOP_FILE)


def render_sop_message(sop: dict[str, Any], *, safety_message: str = "") -> str:
    message = str(sop.get("message", "")).strip()
    if not message:
        raise SOPLoadError(f"SOP {sop.get('id', '<unknown>')} has no message")
    return message.replace("{safety_message}", safety_message or DEFAULT_SAFETY_MESSAGE)
