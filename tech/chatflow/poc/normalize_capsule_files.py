from __future__ import annotations

import argparse
import shutil
from datetime import datetime
from pathlib import Path
from typing import Any

import yaml

from capsule_loader import CAPSULE_DIR, REPO_ROOT, extract_frontmatter, load_capsules


BACKUP_ROOT = Path.home() / ".copilot" / "session-state" / "755dd004-d37d-4ef4-997d-65b328c740e3" / "files" / "backups"

NORMALIZED_MARKER = "原始正文备份"


def find_pristine_source() -> Path | None:
    """Locate the earliest pre-normalize backup (the one holding raw, un-nested drafts).

    A pristine backup is identified by the absence of the normalization marker; this keeps
    re-runs idempotent (we always source the original draft, never a nested normalized copy).
    """
    candidates = sorted(BACKUP_ROOT.glob("capsules-before-format-normalize-*"))
    for candidate in candidates:
        md_files = list(candidate.glob("*.md"))
        if not md_files:
            continue
        if any(NORMALIZED_MARKER in path.read_text(encoding="utf-8") for path in md_files):
            continue
        return candidate
    return None


def original_body_for(capsule: Any, current_body: str, pristine_dir: Path | None) -> str:
    """Return the true raw draft body, preferring the pristine backup over the (possibly
    nested) in-repo body so re-running the normalizer never deepens the backup nesting."""
    if pristine_dir is not None:
        pristine_path = pristine_dir / Path(capsule.path).name
        if pristine_path.exists():
            _fm, body = extract_frontmatter(pristine_path.read_text(encoding="utf-8"))
            return body
    return current_body


def clean_empty(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: clean_empty(val) for key, val in value.items()}
    if isinstance(value, list):
        return [clean_empty(item) for item in value]
    return value


def frontmatter_for(capsule: Any) -> dict[str, Any]:
    ground = capsule.ground or {}
    routing = capsule.routing or {}
    source = capsule.source or []
    return clean_empty(
        {
            "id": capsule.id,
            "title": capsule.title,
            "tree_code": capsule.tree_code,
            "status": capsule.status or "draft",
            "triggers": capsule.triggers,
            "use_when": capsule.use_when,
            "do_not_use_when": capsule.do_not_use_when,
            "recognize": {
                "purpose": capsule.recognize.get("purpose", ""),
                "points": capsule.recognize.get("points", []),
            },
            "act": {
                "purpose": capsule.act.get("purpose", ""),
                "steps": capsule.act.get("steps", []),
            },
            "ground": {
                "summary": ground.get("summary", ""),
                "legal_basis": ground.get("legal_basis", []),
                "practice_basis": ground.get("practice_basis", []),
                "nodes": ground.get("nodes", []),
                "limits": ground.get("limits", []),
            },
            "render_policy": capsule.render_policy or {"ground": "on_demand", "ground_triggers": []},
            "scripts": capsule.scripts,
            "safety_note": capsule.safety_note,
            "routing": {
                "exit_to": routing.get("exit_to", []),
                "related": routing.get("related", []),
            },
            "source": source,
            "review": {
                "schema_version": "v1",
                "content_status": "format-normalized; legal-content-not-reviewed",
                "notes": [
                    "机械格式归一:统一 frontmatter、字段名、字段位置和 R/A/G 形状。",
                    "ground 分为 summary(总体依据)/legal_basis(法律依据)/practice_basis(实践/NGO 经验依据)/nodes(wiki节点id)/limits(边界)。",
                    "原始正文保留在下方代码块,运行时不读取。",
                ],
            },
        }
    )


def normalized_body(capsule: Any, original_body: str) -> str:
    escaped_body = original_body.strip()
    return (
        f"# {capsule.tree_code} {capsule.title}\n\n"
        "> 本文件已按 schema v1 做机械格式归一。运行时只读取 YAML frontmatter;下方原始正文仅供人工复核。\n\n"
        "## 原始正文备份（不参与运行）\n\n"
        "````markdown\n"
        f"{escaped_body}\n"
        "````\n"
    )


def write_capsule(capsule: Any, dry_run: bool, pristine_dir: Path | None) -> None:
    path = REPO_ROOT / capsule.path
    raw = path.read_text(encoding="utf-8")
    _frontmatter, body = extract_frontmatter(raw)
    original_body = original_body_for(capsule, body, pristine_dir)
    fm = yaml.safe_dump(frontmatter_for(capsule), allow_unicode=True, sort_keys=False, width=120)
    new_text = f"---\n{fm}---\n\n{normalized_body(capsule, original_body)}"
    if dry_run:
        print(f"would normalize {path.relative_to(REPO_ROOT)}")
        return
    path.write_text(new_text, encoding="utf-8")
    print(f"normalized {path.relative_to(REPO_ROOT)}")


def backup_capsules() -> Path:
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    backup_dir = BACKUP_ROOT / f"capsules-before-format-normalize-{timestamp}"
    backup_dir.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(CAPSULE_DIR, backup_dir)
    return backup_dir


def main() -> None:
    parser = argparse.ArgumentParser(description="Normalize capsule files to schema v1 frontmatter.")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    pristine_dir = find_pristine_source()
    if pristine_dir is not None:
        print(f"raw-source={pristine_dir}")
    else:
        print("raw-source=<none found; using current in-repo body>")

    capsules = load_capsules()
    if not args.dry_run:
        backup_dir = backup_capsules()
        print(f"backup={backup_dir}")
    for capsule in capsules:
        write_capsule(capsule, args.dry_run, pristine_dir)


if __name__ == "__main__":
    main()
