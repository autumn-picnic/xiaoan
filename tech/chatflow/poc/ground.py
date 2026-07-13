from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


REPO_ROOT = Path(__file__).resolve().parents[3]
WIKI_NODE_DIR = REPO_ROOT / "knowledge" / "wiki" / "nodes"
SOURCE_DIR = REPO_ROOT / "knowledge" / "source"
CAPSULES_JSON = Path(__file__).resolve().parent / "capsules.json"

ARTICLE_RE = re.compile(r"^\s*第[一二三四五六七八九十百千万零〇两0-9]+条")


@dataclass
class GroundItem:
    ref: str
    title: str
    source_ref: str
    text: str
    note: str = ""

    def to_json(self) -> dict[str, str]:
        return {
            "ref": self.ref,
            "title": self.title,
            "source_ref": self.source_ref,
            "text": self.text,
            "note": self.note,
        }


class GroundResolutionError(ValueError):
    pass


def read_text(path: Path) -> str:
    if not path.exists():
        raise GroundResolutionError(f"file not found: {path.relative_to(REPO_ROOT)}")
    return path.read_text(encoding="utf-8")


def extract_frontmatter(text: str) -> str:
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n?", text, re.DOTALL)
    return match.group(1) if match else ""


def extract_title(markdown: str, fallback: str) -> str:
    match = re.search(r"(?m)^title:\s*[\"']?(.+?)[\"']?\s*$", extract_frontmatter(markdown))
    if match:
        return match.group(1).strip()
    heading = re.search(r"(?m)^#\s+(.+?)\s*$", markdown)
    return heading.group(1).strip() if heading else fallback


def strip_frontmatter(markdown: str) -> str:
    return re.sub(r"^---\s*\n.*?\n---\s*\n?", "", markdown, count=1, flags=re.DOTALL).strip()


def extract_source_refs(node_text: str) -> set[str]:
    refs = set(re.findall(r'"(knowledge/source/[^"#]+\.md#[^"]+)"', node_text))
    refs.update(re.findall(r"-\s*(knowledge/source/[^#\s]+\.md#[^\s]+)", node_text))
    return refs


def normalized_anchor(text: str) -> str:
    return re.sub(r"[\s#、，,。.:：()（）《》<>\"'`【】\[\]-]+", "", text).lower()


def normalized_case_anchor(text: str) -> str:
    normalized = normalized_anchor(text)
    chinese_case_numbers = {
        "一": "1",
        "二": "2",
        "三": "3",
        "四": "4",
        "五": "5",
        "六": "6",
        "七": "7",
        "八": "8",
        "九": "9",
        "十": "10",
    }
    return re.sub(
        r"案例([一二三四五六七八九十]+)",
        lambda match: f"案例{chinese_case_numbers.get(match.group(1), match.group(1))}",
        normalized,
    )


def case_anchor_matches(target: str, title: str) -> bool:
    target_case = re.match(r"^案例(\d+)(?:$|\D)", target)
    title_case = re.match(r"^案例(\d+)(?:$|\D)", title)
    if target_case and title_case:
        return target_case.group(1) == title_case.group(1)
    return target in title or title in target


def heading_level(line: str) -> int:
    match = re.match(r"^(#{1,6})\s+", line)
    return len(match.group(1)) if match else 0


def extract_markdown_section(markdown: str, anchor: str) -> str:
    lines = markdown.splitlines()
    if "/" in anchor:
        parent_anchor, child_anchor = (part.strip() for part in anchor.split("/", 1))
        parent_target = normalized_anchor(parent_anchor)
        parent_matches: list[tuple[int, int]] = []
        for idx, line in enumerate(lines):
            level = heading_level(line)
            if not level:
                continue
            title = re.sub(r"^#{1,6}\s+", "", line).strip()
            if normalized_anchor(title) == parent_target:
                parent_matches.append((idx, level))
        if len(parent_matches) != 1:
            return ""
        parent_idx, parent_level = parent_matches[0]

        child_target = normalized_case_anchor(child_anchor)
        child_matches: list[tuple[int, int]] = []
        for idx in range(parent_idx + 1, len(lines)):
            line = lines[idx]
            level = heading_level(line)
            if level and level <= parent_level:
                break
            if not level:
                continue
            title = re.sub(r"^#{1,6}\s+", "", line).strip()
            normalized_title = normalized_case_anchor(title)
            if not case_anchor_matches(child_target, normalized_title):
                continue
            child_matches.append((idx, level))
        if len(child_matches) != 1:
            return ""

        child_idx, child_level = child_matches[0]
        collected = [lines[child_idx].strip()]
        for next_line in lines[child_idx + 1 :]:
            next_level = heading_level(next_line)
            if next_level and next_level <= child_level:
                break
            collected.append(next_line.rstrip())
        return "\n".join(collected).strip()

    target = normalized_anchor(anchor)
    for idx, line in enumerate(lines):
        level = heading_level(line)
        if not level:
            continue
        title = re.sub(r"^#{1,6}\s+", "", line).strip()
        normalized_title = normalized_anchor(title)
        if target not in normalized_title and normalized_title not in target:
            continue
        collected = [line.strip()]
        for next_line in lines[idx + 1 :]:
            next_level = heading_level(next_line)
            if next_level and next_level <= level:
                break
            collected.append(next_line.rstrip())
        return "\n".join(collected).strip()
    return ""


def find_normalized_line(lines: list[str], target: str) -> int | None:
    normalized_target = normalized_anchor(target)
    if not normalized_target:
        return None
    for idx, line in enumerate(lines):
        if normalized_target in normalized_anchor(line):
            return idx
    return None


def extract_article_after(source_text: str, article: str, start_at: int = 0) -> str:
    lines = source_text.splitlines()
    start = None
    for idx in range(start_at, len(lines)):
        line = lines[idx]
        if article in line and ARTICLE_RE.match(line):
            start = idx
            break
    if start is None:
        for idx in range(start_at, len(lines)):
            if article in lines[idx]:
                start = idx
                break
    if start is None:
        raise GroundResolutionError(f"article not found in source: {article}")

    collected = [lines[start].strip()]
    for line in lines[start + 1 :]:
        if ARTICLE_RE.match(line):
            break
        if line.strip():
            collected.append(line.strip())
    return "\n".join(collected).strip()


def extract_source_excerpt(source_text: str, anchor: str) -> str:
    section = extract_markdown_section(source_text, anchor)
    if section:
        return section

    article_match = re.search(r"(第[一二三四五六七八九十百千万零〇两0-9]+条)$", anchor)
    if article_match:
        article = article_match.group(1)
        context = anchor[: article_match.start()].strip()
        start_at = 0
        if context:
            context_line = find_normalized_line(source_text.splitlines(), context)
            if context_line is not None:
                start_at = context_line
        return extract_article_after(source_text, article, start_at)

    line_idx = find_normalized_line(source_text.splitlines(), anchor)
    if line_idx is None:
        raise GroundResolutionError(f"anchor not found in source: {anchor}")
    lines = source_text.splitlines()
    end = min(line_idx + 8, len(lines))
    return "\n".join(line.strip() for line in lines[line_idx:end] if line.strip()).strip()


def resolve_source_ref(source_ref: str, note: str = "") -> GroundItem:
    if "#" not in source_ref:
        raise GroundResolutionError(f"source_ref missing #anchor: {source_ref}")
    path_text, anchor = source_ref.split("#", 1)
    source_prefix = "knowledge/source/"
    if not path_text.startswith(source_prefix):
        raise GroundResolutionError(f"unsupported source_ref path: {source_ref}")
    source_file = path_text[len(source_prefix) :]
    source_path = SOURCE_DIR / source_file
    source_text = read_text(source_path)
    excerpt = extract_source_excerpt(source_text, anchor)
    return GroundItem(
        ref=source_ref,
        title=f"{source_file}#{anchor}",
        source_ref=source_ref,
        text=excerpt,
        note=note,
    )


def resolve_node_context(node_id: str, note: str = "") -> list[GroundItem]:
    """Load a wiki node, then load the source excerpts declared by that node."""
    node_path = WIKI_NODE_DIR / f"{node_id}.md"
    node_text = read_text(node_path)
    node_title = extract_title(node_text, node_id)
    node_item = GroundItem(
        ref=node_id,
        title=node_title,
        source_ref=str(node_path.relative_to(REPO_ROOT)),
        text=strip_frontmatter(node_text),
        note=note or "wiki node context",
    )
    items = [node_item]
    for source_ref in sorted(extract_source_refs(node_text)):
        items.append(resolve_source_ref(source_ref, note=f"source excerpt for node:{node_id}"))
    return items


def resolve_capsule_nodes(capsule: dict[str, Any]) -> list[GroundItem]:
    items: list[GroundItem] = []
    seen_refs: set[str] = set()
    for node_id in capsule.get("ground", {}).get("nodes", []) or []:
        if not node_id:
            continue
        for item in resolve_node_context(node_id):
            if item.ref in seen_refs:
                continue
            seen_refs.add(item.ref)
            items.append(item)
    return items


def resolve_capsule_ground(capsule: dict[str, Any]) -> list[GroundItem]:
    return resolve_capsule_nodes(capsule)


def load_capsules() -> list[dict[str, Any]]:
    if not CAPSULES_JSON.exists():
        raise GroundResolutionError(
            "capsules.json not found; run `python tech/chatflow/poc/capsule_loader.py` first"
        )
    return json.loads(CAPSULES_JSON.read_text(encoding="utf-8"))


def find_capsule(capsule_id: str) -> dict[str, Any]:
    for capsule in load_capsules():
        if capsule.get("id") == capsule_id:
            return capsule
    raise GroundResolutionError(f"capsule not found: {capsule_id}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Resolve legal ground from wiki node ids.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--node", help="Resolve a single wiki node id.")
    group.add_argument("--capsule", help="Resolve all ground nodes for a capsule id.")
    args = parser.parse_args()

    if args.node:
        items = resolve_node_context(args.node)
    else:
        items = resolve_capsule_ground(find_capsule(args.capsule))

    print(json.dumps([item.to_json() for item in items], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
