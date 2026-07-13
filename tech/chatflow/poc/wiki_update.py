from __future__ import annotations

import argparse
import hashlib
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ground import GroundResolutionError, extract_source_refs, resolve_source_ref


REPO_ROOT = Path(__file__).resolve().parents[3]
SOURCE_DIR = REPO_ROOT / "knowledge" / "source"
WIKI_DIR = REPO_ROOT / "knowledge" / "wiki"
DEFAULT_MANIFEST = WIKI_DIR / "source-manifest.json"
DEFAULT_REPORT = WIKI_DIR / "wiki-update-report.md"


@dataclass
class WikiPageRefs:
    path: str
    refs: list[str]
    changed_sources: list[str]


@dataclass
class BrokenRef:
    page: str
    ref: str
    error: str


def repo_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def current_source_manifest() -> dict[str, Any]:
    sources: dict[str, dict[str, Any]] = {}
    for path in sorted(SOURCE_DIR.glob("*.md")):
        sources[repo_path(path)] = {
            "sha256": file_sha256(path),
            "size_bytes": path.stat().st_size,
        }
    return {
        "version": 1,
        "updated_at": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "sources": sources,
    }


def load_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"version": 1, "updated_at": "", "sources": {}}
    return json.loads(path.read_text(encoding="utf-8"))


def diff_sources(previous: dict[str, Any], current: dict[str, Any]) -> dict[str, list[str]]:
    previous_sources = previous.get("sources", {})
    current_sources = current.get("sources", {})
    previous_paths = set(previous_sources)
    current_paths = set(current_sources)
    added = sorted(current_paths - previous_paths)
    deleted = sorted(previous_paths - current_paths)
    modified = sorted(
        path
        for path in previous_paths & current_paths
        if previous_sources[path].get("sha256") != current_sources[path].get("sha256")
    )
    unchanged = sorted(
        path
        for path in previous_paths & current_paths
        if previous_sources[path].get("sha256") == current_sources[path].get("sha256")
    )
    return {
        "added": added,
        "modified": modified,
        "deleted": deleted,
        "unchanged": unchanged,
    }


def wiki_markdown_files(report_path: Path) -> list[Path]:
    skipped = {report_path.resolve(), DEFAULT_MANIFEST.resolve()}
    return [
        path
        for path in sorted(WIKI_DIR.rglob("*.md"))
        if path.resolve() not in skipped and path.is_file()
    ]


def source_path_from_ref(source_ref: str) -> str:
    return source_ref.split("#", 1)[0]


def analyze_wiki_refs(changed_sources: set[str], report_path: Path) -> tuple[list[WikiPageRefs], list[BrokenRef], dict[str, list[str]]]:
    affected_pages: list[WikiPageRefs] = []
    broken_refs: list[BrokenRef] = []
    ref_index: dict[str, list[str]] = {}

    for path in wiki_markdown_files(report_path):
        page = repo_path(path)
        text = path.read_text(encoding="utf-8")
        refs = sorted(extract_source_refs(text))
        if not refs:
            continue

        page_changed_sources = sorted({source_path_from_ref(ref) for ref in refs if source_path_from_ref(ref) in changed_sources})
        if page_changed_sources:
            affected_pages.append(WikiPageRefs(page, refs, page_changed_sources))

        for ref in refs:
            ref_index.setdefault(source_path_from_ref(ref), []).append(page)
            try:
                resolve_source_ref(ref)
            except GroundResolutionError as exc:
                broken_refs.append(BrokenRef(page=page, ref=ref, error=str(exc)))

    return affected_pages, broken_refs, ref_index


def markdown_list(items: list[str]) -> list[str]:
    return [f"- `{item}`" for item in items] if items else ["- none"]


def render_report(
    *,
    manifest_path: Path,
    previous: dict[str, Any],
    current: dict[str, Any],
    source_diff: dict[str, list[str]],
    affected_pages: list[WikiPageRefs],
    broken_refs: list[BrokenRef],
    unreferenced_changed_sources: list[str],
    manifest_written: bool,
) -> str:
    changed_count = sum(len(source_diff[key]) for key in ("added", "modified", "deleted"))
    lines: list[str] = [
        "# Wiki Update Report",
        "",
        f"- generated_at: `{datetime.now(UTC).replace(microsecond=0).isoformat()}`",
        f"- manifest: `{repo_path(manifest_path)}`",
        f"- previous_manifest_updated_at: `{previous.get('updated_at') or 'none'}`",
        f"- current_source_count: {len(current.get('sources', {}))}",
        f"- changed_source_count: {changed_count}",
        f"- manifest_written: {str(manifest_written).lower()}",
        "",
        "## Source changes",
        "",
        "| status | count |",
        "|---|---:|",
        f"| added | {len(source_diff['added'])} |",
        f"| modified | {len(source_diff['modified'])} |",
        f"| deleted | {len(source_diff['deleted'])} |",
        "",
        "### Added",
        *markdown_list(source_diff["added"]),
        "",
        "### Modified",
        *markdown_list(source_diff["modified"]),
        "",
        "### Deleted",
        *markdown_list(source_diff["deleted"]),
        "",
        "## Affected wiki pages",
        "",
    ]

    if affected_pages:
        lines.extend(["| page | changed source files |", "|---|---|"])
        for item in affected_pages:
            changed = "<br>".join(f"`{source}`" for source in item.changed_sources)
            lines.append(f"| `{item.path}` | {changed} |")
    else:
        lines.append("- none")

    lines.extend(["", "## Broken source_refs", ""])
    if broken_refs:
        lines.extend(["| page | source_ref | error |", "|---|---|---|"])
        for item in broken_refs:
            lines.append(f"| `{item.page}` | `{item.ref}` | {item.error} |")
    else:
        lines.append("- none")

    lines.extend(["", "## Changed source files with no wiki references", ""])
    lines.extend(markdown_list(unreferenced_changed_sources))

    lines.extend(
        [
            "",
            "## Manual update workflow",
            "",
            "1. Review added/modified/deleted source files above.",
            "2. For each affected wiki page, update `knowledge/wiki/nodes/*.md`, `edges.md`, or syntheses as needed.",
            "3. For added sources with no wiki references, decide whether to create a new node or attach the source to existing nodes.",
            "4. For deleted sources, remove or replace stale `source_refs` before running chatflow.",
            "5. Re-run this script until broken refs are gone.",
            "6. After the wiki layer is updated and reviewed, re-run with `--write-manifest` to accept the current source snapshot.",
            "",
            "Suggested command:",
            "",
            "```bash",
            ".venv/bin/python tech/chatflow/poc/wiki_update.py",
            ".venv/bin/python tech/chatflow/poc/wiki_update.py --write-manifest",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect source changes and generate a wiki update report.")
    parser.add_argument("--manifest", default=str(DEFAULT_MANIFEST), help="Path to the source snapshot manifest.")
    parser.add_argument("--report", default=str(DEFAULT_REPORT), help="Path to write the update report.")
    parser.add_argument("--write-manifest", action="store_true", help="Accept current sources as the new baseline.")
    parser.add_argument("--json", action="store_true", help="Print a machine-readable summary.")
    parser.add_argument("--fail-on-drift", action="store_true", help="Exit non-zero if sources changed or refs are broken.")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    report_path = Path(args.report)
    previous = load_manifest(manifest_path)
    current = current_source_manifest()
    source_diff = diff_sources(previous, current)
    changed_sources = set(source_diff["added"] + source_diff["modified"] + source_diff["deleted"])
    affected_pages, broken_refs, ref_index = analyze_wiki_refs(changed_sources, report_path)
    unreferenced_changed_sources = sorted(source for source in changed_sources if source not in ref_index)

    if args.write_manifest:
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    report = render_report(
        manifest_path=manifest_path,
        previous=previous,
        current=current,
        source_diff=source_diff,
        affected_pages=affected_pages,
        broken_refs=broken_refs,
        unreferenced_changed_sources=unreferenced_changed_sources,
        manifest_written=args.write_manifest,
    )
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(report, encoding="utf-8")

    summary = {
        "report": repo_path(report_path),
        "manifest": repo_path(manifest_path),
        "manifest_written": args.write_manifest,
        "added": len(source_diff["added"]),
        "modified": len(source_diff["modified"]),
        "deleted": len(source_diff["deleted"]),
        "affected_pages": len(affected_pages),
        "broken_refs": len(broken_refs),
        "unreferenced_changed_sources": len(unreferenced_changed_sources),
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2) if args.json else "\n".join(f"{key}={value}" for key, value in summary.items()))

    if args.fail_on_drift and (
        source_diff["added"] or source_diff["modified"] or source_diff["deleted"] or broken_refs
    ):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
