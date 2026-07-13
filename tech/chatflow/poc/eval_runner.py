from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from ground import GroundResolutionError, resolve_node_context
from pii_redactor import redact_pii
from render_policy import should_load_ground
from router import BASELINE_CAPSULE_ID, load_capsules, select_router
from safety import scan_safety
from sop_loader import load_baseline_sop, load_crisis_sop


REPO_ROOT = Path(__file__).resolve().parents[3]
EVAL_DIR = Path(__file__).resolve().parent / "eval"
DEFAULT_QUESTIONS = EVAL_DIR / "questions.jsonl"
DEFAULT_REPORT = EVAL_DIR / "smoke-report.md"
CRISIS_SOP_ID = "crisis_sop"


def load_questions(path: Path) -> list[dict[str, Any]]:
    questions: list[dict[str, Any]] = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            questions.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSONL at {path}:{line_number}: {exc}") from exc
    return questions


def find_capsule(capsules: list[dict[str, Any]], capsule_id: str) -> dict[str, Any]:
    if capsule_id == BASELINE_CAPSULE_ID:
        return load_baseline_sop()
    if capsule_id == CRISIS_SOP_ID:
        return load_crisis_sop()
    for capsule in capsules:
        if capsule.get("id") == capsule_id:
            return capsule
    raise ValueError(f"capsule not found: {capsule_id}")


def count_ground_errors(capsule: dict[str, Any], message: str) -> int:
    if capsule.get("id") in {BASELINE_CAPSULE_ID, CRISIS_SOP_ID}:
        return 0
    should_load, _ = should_load_ground(capsule, message)
    if not should_load:
        return 0
    ground = capsule.get("ground", {})
    errors = 0
    for node_id in ground.get("nodes", []) or []:
        try:
            resolve_node_context(node_id)
        except GroundResolutionError:
            errors += 1
    has_ground = bool(
        ground.get("summary")
        or ground.get("legal_basis")
        or ground.get("practice_basis")
        or ground.get("nodes")
    )
    if not has_ground:
        errors += 1
    return errors


def run_eval(questions: list[dict[str, Any]], offline: bool, model: str) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    capsules = load_capsules()
    capsule_router = select_router(offline=offline, model=model)
    results: list[dict[str, Any]] = []
    for question in questions:
        redaction = redact_pii(question["message"])
        safety = scan_safety(question["message"])
        if safety.is_red_flag:
            capsule_id = CRISIS_SOP_ID
            confidence = 1.0
            method = "crisis_sop"
            reason = safety.reason
        else:
            decision = capsule_router.route(redaction.redacted_text, capsules=capsules)
            capsule_id = decision.capsule_id
            confidence = decision.confidence
            method = decision.method
            reason = decision.reason
        selected = find_capsule(capsules, capsule_id)
        expected = question.get("expected_capsule_id", "")
        expected_safety = question.get("expected_safety_level", "")
        result = {
            "id": question["id"],
            "redacted_message": redaction.redacted_text,
            "pii_tag_count": len(redaction.tags),
            "safety_level": safety.level,
            "expected_safety_level": expected_safety,
            "safety_ok": not expected_safety or safety.level == expected_safety,
            "expected": expected,
            "actual": capsule_id,
            "route_ok": capsule_id == expected,
            "confidence": confidence,
            "method": method,
            "reason": reason,
            "ground_error_count": count_ground_errors(selected, redaction.redacted_text),
            "selected_issue_count": len(selected.get("issues", [])),
        }
        results.append(result)

    total = len(results)
    route_ok = sum(1 for item in results if item["route_ok"])
    safety_expected = [item for item in results if item["expected_safety_level"]]
    safety_ok = sum(1 for item in safety_expected if item["safety_ok"])
    selected_ground_errors = sum(item["ground_error_count"] for item in results)
    summary = {
        "total": total,
        "route_ok": route_ok,
        "route_accuracy": route_ok / total if total else 0,
        "safety_checked": len(safety_expected),
        "safety_ok": safety_ok,
        "selected_ground_errors": selected_ground_errors,
    }
    return results, summary


def write_report(results: list[dict[str, Any]], summary: dict[str, Any], path: Path) -> None:
    lines = [
        "# MVP Smoke Eval Report",
        "",
        f"- total: {summary['total']}",
        f"- route_ok: {summary['route_ok']}",
        f"- route_accuracy: {summary['route_accuracy']:.0%}",
        f"- safety_ok: {summary['safety_ok']}/{summary['safety_checked']}",
        f"- selected_ground_errors: {summary['selected_ground_errors']}",
        "",
        "| id | expected | actual | route | safety | pii | confidence | ground errors | issues |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for item in results:
        ok = "✅" if item["route_ok"] else "❌"
        safety_ok = "✅" if item["safety_ok"] else "❌"
        lines.append(
            f"| {item['id']} | `{item['expected']}` | `{item['actual']}` | {ok} | {safety_ok} | "
            f"{item['pii_tag_count']} | "
            f"{item['confidence']:.2f} | {item['ground_error_count']} | {item['selected_issue_count']} |"
        )
    lines.extend(["", "## Details", ""])
    for item in results:
        lines.append(f"### {item['id']}")
        lines.append(f"- redacted_message: {item['redacted_message']}")
        lines.append(f"- safety: `{item['safety_level']}`")
        lines.append(f"- route: `{item['actual']}` (expected `{item['expected']}`), confidence {item['confidence']:.2f}")
        lines.append(f"- reason: {item['reason']}")
        lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run XiaoAn MVP smoke eval.")
    parser.add_argument("--questions", default=str(DEFAULT_QUESTIONS))
    parser.add_argument("--report", default=str(DEFAULT_REPORT))
    parser.add_argument("--model", default="gpt-4o-mini")
    parser.add_argument("--offline", action="store_true", help="Use offline heuristic router.")
    args = parser.parse_args()

    questions = load_questions(Path(args.questions))
    results, summary = run_eval(questions, offline=args.offline, model=args.model)
    write_report(results, summary, Path(args.report))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print(f"report={Path(args.report).relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
