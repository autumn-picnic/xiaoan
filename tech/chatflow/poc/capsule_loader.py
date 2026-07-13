from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[3]
CAPSULE_DIR = REPO_ROOT / "knowledge" / "capsules"
WIKI_NODE_DIR = REPO_ROOT / "knowledge" / "wiki" / "nodes"
OUT_DIR = Path(__file__).resolve().parent

REQUIRED_TOP_LEVEL = [
    "id",
    "title",
    "tree_code",
    "status",
    "triggers",
    "use_when",
    "do_not_use_when",
    "recognize",
    "act",
    "ground",
]

KNOWN_SECTION_KEYS = {
    "triggers",
    "use_when",
    "fits_any",
    "do_not_use_when",
    "content",
    "steps",
    "scripts",
    "safety_note",
    "legal_basis",
    "practice_basis",
    "limits",
    "source",
    "routing",
    "related_capsules",
    "name",
}


@dataclass
class CapsuleIssue:
    level: str
    message: str


@dataclass
class ParsedCapsule:
    path: str
    id: str
    title: str
    tree_code: str
    status: str
    triggers: list[str] = field(default_factory=list)
    use_when: list[str] = field(default_factory=list)
    do_not_use_when: list[str] = field(default_factory=list)
    recognize: dict[str, Any] = field(default_factory=dict)
    act: dict[str, Any] = field(default_factory=dict)
    ground: dict[str, Any] = field(default_factory=dict)
    render_policy: dict[str, Any] = field(default_factory=dict)
    scripts: list[Any] = field(default_factory=list)
    safety_note: list[str] = field(default_factory=list)
    routing: dict[str, Any] = field(default_factory=dict)
    source: list[Any] = field(default_factory=list)
    review: dict[str, Any] = field(default_factory=dict)
    issues: list[CapsuleIssue] = field(default_factory=list)

    def to_json(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "id": self.id,
            "title": self.title,
            "tree_code": self.tree_code,
            "status": self.status,
            "triggers": self.triggers,
            "use_when": self.use_when,
            "do_not_use_when": self.do_not_use_when,
            "recognize": self.recognize,
            "act": self.act,
            "ground": self.ground,
            "render_policy": self.render_policy,
            "scripts": self.scripts,
            "safety_note": self.safety_note,
            "routing": self.routing,
            "source": self.source,
            "review": self.review,
            "issues": [issue.__dict__ for issue in self.issues],
        }


def clean_value(value: str) -> str:
    value = value.strip()
    value = re.sub(r"\s+#.*$", "", value)
    value = value.rstrip(",，")
    value = value.strip()
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        value = value[1:-1]
    return value.strip()


def is_placeholder(value: str) -> bool:
    lowered = value.lower()
    return (
        not value
        or value.strip() in {">", "|"}
        or "【挂起】" in value
        or "暂缺" in value
        or lowered in {"none", "null"}
        or lowered.startswith(("q:", "q："))
        or value.startswith("要求：")
        or value.startswith("格式：")
        or value.startswith("说明：")
        or value.startswith("示例：")
    )


def normalize_scalar(value: Any) -> str:
    if value is None:
        return ""
    cleaned = clean_value(str(value))
    return "" if is_placeholder(cleaned) else cleaned


def extract_frontmatter(text: str) -> tuple[str, str]:
    if not text.startswith("---"):
        return "", text
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    if not match:
        return "", text
    return match.group(1), text[match.end() :]


def normalize_string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        normalized: list[str] = []
        for item in value:
            if isinstance(item, str):
                cleaned = clean_value(item)
                if cleaned and not is_placeholder(cleaned):
                    normalized.append(cleaned)
            elif isinstance(item, dict):
                cleaned = " ".join(str(part) for part in item.values() if part)
                cleaned = clean_value(cleaned)
                if cleaned and not is_placeholder(cleaned):
                    normalized.append(cleaned)
        return normalized
    if isinstance(value, str):
        cleaned = clean_value(value)
        return [cleaned] if cleaned and not is_placeholder(cleaned) else []
    return []


def normalize_steps(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        steps: list[Any] = []
        for item in value:
            if isinstance(item, str):
                cleaned = clean_value(item)
                if cleaned and not is_placeholder(cleaned):
                    step_match = re.match(r"^step\s*:\s*[\"']?(.+?)[\"']?$", cleaned)
                    if step_match:
                        steps.append({"action": clean_value(step_match.group(1)), "detail": ""})
                    else:
                        steps.append(cleaned)
            elif isinstance(item, dict):
                cleaned_item = {
                    str(key): str(val).strip()
                    for key, val in item.items()
                    if val is not None and str(val).strip()
                }
                if cleaned_item:
                    steps.append(cleaned_item)
        return steps
    if isinstance(value, str):
        return normalize_string_list(value)
    return []


def parse_v1_frontmatter(path: Path, frontmatter: str) -> ParsedCapsule | None:
    if not frontmatter.strip():
        return None
    try:
        data = yaml.safe_load(frontmatter) or {}
    except yaml.YAMLError:
        return None
    if not isinstance(data, dict):
        return None
    if not data.get("id") or not data.get("tree_code"):
        return None

    recognize_data = data.get("recognize") if isinstance(data.get("recognize"), dict) else {}
    act_data = data.get("act") if isinstance(data.get("act"), dict) else {}
    ground_data = data.get("ground") if isinstance(data.get("ground"), dict) else {}
    render_policy_data = data.get("render_policy") if isinstance(data.get("render_policy"), dict) else {}
    routing_data = data.get("routing") if isinstance(data.get("routing"), dict) else {}

    capsule = ParsedCapsule(
        path=str(path.relative_to(REPO_ROOT)),
        id=normalize_scalar(data.get("id")),
        title=normalize_scalar(data.get("title")),
        tree_code=normalize_scalar(data.get("tree_code")),
        status=normalize_scalar(data.get("status")) or "draft",
        triggers=normalize_string_list(data.get("triggers")),
        use_when=normalize_string_list(data.get("use_when")),
        do_not_use_when=normalize_string_list(data.get("do_not_use_when")),
        recognize={
            "purpose": normalize_scalar(recognize_data.get("purpose")),
            "points": normalize_string_list(recognize_data.get("points")),
            "groups": recognize_data.get("groups", []) if isinstance(recognize_data.get("groups"), list) else [],
        },
        act={
            "purpose": normalize_scalar(act_data.get("purpose")),
            "steps": normalize_steps(act_data.get("steps")),
        },
        ground={
            "summary": normalize_scalar(ground_data.get("summary"))
            or normalize_scalar(ground_data.get("purpose")),
            "legal_basis": normalize_string_list(ground_data.get("legal_basis"))
            or normalize_string_list(ground_data.get("legacy_legal_basis")),
            "practice_basis": normalize_string_list(ground_data.get("practice_basis")),
            "limits": normalize_string_list(ground_data.get("limits")),
            "nodes": normalize_string_list(ground_data.get("nodes")),
        },
        render_policy={
            "ground": normalize_scalar(render_policy_data.get("ground")) or "on_demand",
            "ground_triggers": normalize_string_list(render_policy_data.get("ground_triggers")),
        },
        scripts=data.get("scripts", []) if isinstance(data.get("scripts"), list) else [],
        safety_note=normalize_string_list(data.get("safety_note")),
        routing=routing_data,
        source=data.get("source", []) if isinstance(data.get("source"), list) else [],
        review=data.get("review", {}) if isinstance(data.get("review"), dict) else {},
    )
    validate_required(capsule, f"---\n{frontmatter}\n---\n")
    return capsule


def infer_tree_code(path: Path) -> str:
    match = re.match(r"\s*([NK][0-9A-Za-z]+)", path.stem)
    if match:
        return match.group(1)
    return path.stem.split()[0].replace("：", "").replace(":", "")


def infer_id(tree_code: str) -> str:
    return re.sub(r"[^0-9a-z]+", "", tree_code.lower())


def extract_scalar(text: str, key: str) -> str:
    escaped = re.escape(key)
    patterns = [
        rf"(?m)^\s*\*\*{escaped}:\*\*\s*(.+?)\s*$",
        rf"(?m)^\s*\*\*{escaped}\*\*:\s*(.+?)\s*$",
        rf"(?m)^\s*{escaped}\s*:\s*(.+?)\s*$",
    ]
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            value = clean_value(match.group(1))
            if not is_placeholder(value):
                return value

    # Some drafts split keys and colons across lines, e.g. "act.purpose" then ": value".
    lines = text.splitlines()
    for idx, line in enumerate(lines[:-1]):
        if line.strip() == key and lines[idx + 1].lstrip().startswith(":"):
            value = clean_value(lines[idx + 1].split(":", 1)[1])
            if not is_placeholder(value):
                return value
    return ""


def extract_heading(text: str) -> str:
    match = re.search(r"(?m)^#\s+(.+?)\s*$", text)
    return clean_value(match.group(1)) if match else ""


def find_key_line(lines: list[str], key: str) -> int | None:
    escaped = re.escape(key)
    pattern = re.compile(rf"^\s*(?:#\s*)?{escaped}\s*:?\s*(?:[#*（(].*)?$")
    for idx, line in enumerate(lines):
        if pattern.match(line.strip()):
            return idx
        if re.match(rf"^\s*{escaped}\s*:\s*.+", line):
            return idx
    return None


def collect_block(text: str, key: str) -> list[str]:
    lines = text.splitlines()
    start = find_key_line(lines, key)
    if start is None:
        return []

    block: list[str] = []
    first = lines[start]
    if ":" in first:
        inline = first.split(":", 1)[1].strip()
        if inline and not inline.startswith(("|", ">")):
            block.append(inline)

    for line in lines[start + 1 :]:
        stripped = line.strip()
        if not stripped:
            if block:
                break
            continue
        if stripped.startswith("```"):
            continue
        if block and re.match(r"^#{1,6}\s+", stripped):
            break
        if block and re.match(r"^[A-Za-z_][A-Za-z0-9_.]*\s*:?\s*$", stripped):
            possible_key = stripped.rstrip(":")
            if possible_key in KNOWN_SECTION_KEYS or "." in possible_key:
                break
        if block and re.match(r"^[A-Za-z_][A-Za-z0-9_.]*\s*:", stripped):
            possible_key = stripped.split(":", 1)[0]
            if possible_key in KNOWN_SECTION_KEYS or "." in possible_key:
                break
        block.append(line)
    return block


def parse_listish(block: list[str]) -> list[str]:
    values: list[str] = []
    for line in block:
        stripped = line.strip()
        if not stripped or stripped.startswith(("```", "<!--")):
            continue
        if stripped.endswith(":") and not stripped.startswith(("-", '"', "'")):
            continue
        if stripped.startswith(("#", "##")):
            continue
        if stripped.startswith(("要求：", "格式：", "说明：", "示例：")):
            continue

        if stripped.startswith("-"):
            value = stripped[1:].strip()
        elif re.match(r"^\d+[.、]\s+", stripped):
            value = re.sub(r"^\d+[.、]\s+", "", stripped)
        elif stripped.startswith(("\"", "'")):
            value = stripped
        else:
            continue

        value = clean_value(value)
        if value and not is_placeholder(value):
            values.append(value)
    return values


def extract_list(text: str, key: str) -> list[str]:
    return parse_listish(collect_block(text, key))


def extract_v1_recognize_points(text: str) -> list[str]:
    section = collect_section_text(text, "recognize")
    points: list[str] = []
    in_points = False
    for line in section.splitlines():
        stripped = line.strip()
        if stripped == "points:":
            in_points = True
            continue
        if in_points and stripped.startswith("- theme:"):
            in_points = False
        if stripped.startswith("- theme:"):
            continue
        if stripped == "points:":
            in_points = True
            continue
        if in_points and stripped.startswith("-"):
            value = clean_value(stripped[1:].strip())
            if value and not is_placeholder(value):
                points.append(value)
    return points


def extract_v1_steps(text: str) -> list[dict[str, str]]:
    section = collect_section_text(text, "act")
    steps: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in section.splitlines():
        stripped = line.strip()
        action_match = re.match(r"-\s+action:\s*(.+)$", stripped)
        if action_match:
            if current:
                steps.append(current)
            current = {"action": clean_value(action_match.group(1)), "detail": ""}
            continue
        detail_match = re.match(r"detail:\s*(.+)$", stripped)
        if detail_match and current is not None:
            current["detail"] = clean_value(detail_match.group(1))
    if current:
        steps.append(current)
    return steps


def extract_v1_routing(text: str) -> dict[str, Any]:
    targets = [{"to": m.group(1), "when": ""} for m in re.finditer(r"(?m)^\s*-\s+to:\s*([A-Za-z0-9_-]+)\s*$", text)]
    related: list[str] = []
    related_match = re.search(r"(?m)^\s*related:\s*\[(.*?)\]\s*$", text)
    if related_match:
        related = [clean_value(item) for item in related_match.group(1).split(",")]
        related = [item for item in related if item]
    return {"exit_to": targets, "related": related}


def extract_legacy_legal_basis(text: str) -> list[str]:
    return extract_list(text, "legal_basis")


def parse_capsule(path: Path) -> ParsedCapsule:
    raw = path.read_text(encoding="utf-8")
    frontmatter, body = extract_frontmatter(raw)
    v1_capsule = parse_v1_frontmatter(path, frontmatter)
    if v1_capsule:
        return v1_capsule
    combined = frontmatter + "\n" + body

    tree_code = extract_scalar(frontmatter, "tree_code") or infer_tree_code(path)
    capsule_id = extract_scalar(frontmatter, "id") or infer_id(tree_code)
    title = (
        extract_scalar(frontmatter, "title")
        or extract_scalar(combined, "capsule_name")
        or extract_heading(combined)
        or path.stem
    )
    title = re.sub(r"^[NK][0-9A-Za-z]+[:：]?\s*", "", title).strip() or title
    status = extract_scalar(frontmatter, "status") or extract_scalar(combined, "status") or "draft"
    if status.startswith("draft"):
        status = "draft"

    triggers = extract_list(combined, "triggers")
    use_when = extract_list(combined, "use_when") or extract_list(combined, "fits_any")
    do_not_use_when = extract_list(combined, "do_not_use_when")

    recognize_purpose = extract_scalar(combined, "recognize.purpose") or extract_scalar(
        collect_section_text(combined, "recognize"), "purpose"
    )
    recognize_points = extract_v1_recognize_points(frontmatter) or extract_list(combined, "content")
    if not recognize_points:
        recognize_points = extract_list(collect_section_text(combined, "recognize"), "points")

    act_purpose = extract_scalar(combined, "act.purpose") or extract_scalar(
        collect_section_text(combined, "act"), "purpose"
    )
    steps = extract_v1_steps(frontmatter) or extract_list(combined, "steps")

    ground_purpose = extract_scalar(combined, "ground.purpose") or extract_scalar(
        collect_section_text(combined, "ground"), "purpose"
    )
    legacy_legal_basis = extract_legacy_legal_basis(combined)

    capsule = ParsedCapsule(
        path=str(path.relative_to(REPO_ROOT)),
        id=capsule_id,
        title=title,
        tree_code=tree_code,
        status=status,
        triggers=triggers,
        use_when=use_when,
        do_not_use_when=do_not_use_when,
        recognize={"purpose": recognize_purpose, "points": recognize_points},
        act={"purpose": act_purpose, "steps": steps},
        ground={
            "summary": ground_purpose,
            "legal_basis": legacy_legal_basis,
            "practice_basis": extract_list(combined, "practice_basis"),
            "limits": extract_list(combined, "limits"),
            "nodes": [],
        },
        render_policy={"ground": "on_demand", "ground_triggers": []},
        scripts=extract_list(combined, "scripts"),
        safety_note=extract_list(combined, "safety_note"),
        routing=extract_v1_routing(combined),
        source=extract_list(combined, "source") or extract_list(combined, "name"),
    )

    validate_required(capsule, raw)
    return capsule


def collect_section_text(text: str, section_name: str) -> str:
    lines = text.splitlines()
    start = None
    pattern = re.compile(rf"^\s*(?:#+\s*)?(?:\d+\.\s*)?{re.escape(section_name)}(?:\s|[（(:：]|$)", re.I)
    for idx, line in enumerate(lines):
        if pattern.search(line.strip()):
            start = idx
            break
    if start is None:
        return ""
    collected: list[str] = []
    for line in lines[start + 1 :]:
        stripped = line.strip()
        if collected and re.match(r"^#{1,6}\s+", stripped):
            break
        collected.append(line)
    return "\n".join(collected)


def validate_required(capsule: ParsedCapsule, raw: str) -> None:
    checks = {
        "id": bool(capsule.id),
        "title": bool(capsule.title),
        "tree_code": bool(capsule.tree_code),
        "status": bool(capsule.status),
        "triggers": bool(capsule.triggers),
        "use_when": bool(capsule.use_when),
        "do_not_use_when": bool(capsule.do_not_use_when),
        "recognize": bool(capsule.recognize.get("purpose") or capsule.recognize.get("points")),
        "act": bool(capsule.act.get("purpose") or capsule.act.get("steps")),
        "ground": bool(
            capsule.ground.get("summary")
            or capsule.ground.get("legal_basis")
            or capsule.ground.get("practice_basis")
            or capsule.ground.get("nodes")
        ),
    }
    for key in REQUIRED_TOP_LEVEL:
        if not checks[key]:
            capsule.issues.append(CapsuleIssue("error", f"missing required field: {key}"))

    if not raw.startswith("---"):
        capsule.issues.append(CapsuleIssue("warning", "missing frontmatter; parsed from body only"))
    elif "id:" not in raw.split("---", 2)[1]:
        capsule.issues.append(CapsuleIssue("warning", "legacy frontmatter; id inferred from filename"))

    if re.search(r"要求：|格式：|说明：|【挂起】|暂缺", raw):
        capsule.issues.append(CapsuleIssue("warning", "draft/template text remains in capsule"))

    ground_policy = capsule.render_policy.get("ground", "on_demand")
    if ground_policy not in {"on_demand", "always", "on_entry", "never"}:
        capsule.issues.append(CapsuleIssue("error", f"invalid render_policy.ground: {ground_policy}"))


def validate_cross_references(capsules: list[ParsedCapsule]) -> None:
    ids = {capsule.id for capsule in capsules}
    seen: dict[str, str] = {}
    for capsule in capsules:
        if capsule.id in seen:
            capsule.issues.append(CapsuleIssue("error", f"duplicate id also used by {seen[capsule.id]}"))
        seen[capsule.id] = capsule.path

        for node_id in capsule.ground.get("nodes", []) or []:
            if not (WIKI_NODE_DIR / f"{node_id}.md").exists():
                capsule.issues.append(CapsuleIssue("error", f"ground node not found: {node_id}"))

        related = capsule.routing.get("related", [])
        exit_targets = [item.get("to") for item in capsule.routing.get("exit_to", [])]
        for target in [item for item in related + exit_targets if item]:
            if target not in ids:
                capsule.issues.append(CapsuleIssue("warning", f"dangling routing target: {target}"))


def load_capsules() -> list[ParsedCapsule]:
    capsules = [parse_capsule(path) for path in sorted(CAPSULE_DIR.glob("*.md"))]
    validate_cross_references(capsules)
    return capsules


def write_json(capsules: list[ParsedCapsule]) -> Path:
    output_path = OUT_DIR / "capsules.json"
    output_path.write_text(
        json.dumps([capsule.to_json() for capsule in capsules], ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return output_path


def write_report(capsules: list[ParsedCapsule]) -> Path:
    output_path = OUT_DIR / "capsule-normalization-report.md"
    lines: list[str] = [
        "# 胶囊规范化报告",
        "",
        "本报告由 `capsule_loader.py` 生成,用于把现有胶囊草稿收敛到 schema v1。",
        "",
        "## 总览",
        "",
        "| id | title | status | triggers | legal_basis | practice_basis | issues |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for capsule in capsules:
        ground = capsule.ground or {}
        lines.append(
            f"| `{capsule.id}` | {capsule.title} | {capsule.status} | "
            f"{len(capsule.triggers)} | {len(ground.get('legal_basis', []))} | "
            f"{len(ground.get('practice_basis', []))} | {len(capsule.issues)} |"
        )

    lines.extend(["", "## 详细问题", ""])
    for capsule in capsules:
        lines.append(f"### `{capsule.id}` {capsule.title}")
        if capsule.issues:
            for issue in capsule.issues:
                lines.append(f"- **{issue.level}**: {issue.message}")
        else:
            lines.append("- 无结构化问题。")
        lines.append("")

    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return output_path


def main() -> None:
    capsules = load_capsules()
    json_path = write_json(capsules)
    report_path = write_report(capsules)
    error_count = sum(1 for capsule in capsules for issue in capsule.issues if issue.level == "error")
    warning_count = sum(1 for capsule in capsules for issue in capsule.issues if issue.level == "warning")
    print(f"loaded={len(capsules)} errors={error_count} warnings={warning_count}")
    print(f"json={json_path.relative_to(REPO_ROOT)}")
    print(f"report={report_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
