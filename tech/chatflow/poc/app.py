from __future__ import annotations

import argparse
import json
import sys
from typing import Any

from compose import ComposeError, SupportAgent, select_support_agent
from ground import GroundItem, GroundResolutionError, resolve_node_context
from output_guard import guard_output
from pii_redactor import redact_pii
from render_policy import capsule_for_render, should_load_ground
from router import BASELINE_CAPSULE_ID, CapsuleRouter, RouteDecision, RouterError, load_capsules, select_router
from safety import scan_safety
from settings import get_model, masked_api_key
from sop_loader import load_baseline_sop, load_crisis_sop, render_sop_message
from state import ConversationState


CRISIS_SOP_ID = "crisis_sop"


def find_capsule(capsules: list[dict[str, Any]], capsule_id: str) -> dict[str, Any]:
    for capsule in capsules:
        if capsule.get("id") == capsule_id:
            return capsule
    raise RouterError(f"capsule not found after routing: {capsule_id}")


def resolve_ground_with_warnings(capsule: dict[str, Any]) -> tuple[list[GroundItem], list[str]]:
    ground = capsule.get("ground", {})
    items: list[GroundItem] = []
    seen_refs: set[str] = set()
    warnings: list[str] = []
    for node_id in ground.get("nodes", []) or []:
        if not node_id:
            continue
        try:
            for item in resolve_node_context(node_id):
                if item.ref in seen_refs:
                    continue
                seen_refs.add(item.ref)
                items.append(item)
        except GroundResolutionError as exc:
            warnings.append(f"node:{node_id}: {exc}")
    has_ground = bool(
        ground.get("summary")
        or ground.get("legal_basis")
        or ground.get("practice_basis")
        or ground.get("nodes")
    )
    if not has_ground:
        warnings.append("selected capsule has no ground (summary/legal_basis/practice_basis/nodes)")
    return items, warnings


def run_turn(
    message: str,
    capsules: list[dict[str, Any]],
    state: ConversationState | None = None,
    model: str = "",
    offline: bool = False,
    debug: bool = False,
    capsule_router: CapsuleRouter | None = None,
    support_agent: SupportAgent | None = None,
) -> tuple[str, ConversationState]:
    state = state or ConversationState()
    capsule_router = capsule_router or select_router(offline=offline, model=model)
    support_agent = support_agent or select_support_agent(offline=offline, model=model)
    redaction = redact_pii(message)
    safety = scan_safety(message)
    if safety.is_red_flag:
        decision = RouteDecision(
            capsule_id=CRISIS_SOP_ID,
            confidence=1.0,
            reason=f"safety: {safety.reason}",
            should_continue_active_capsule=False,
            method="crisis_sop",
        )
        capsule = load_crisis_sop()
        ground_items = []
        ground_warnings = []
        ground_loaded = False
        ground_policy_reason = "crisis_sop bypass"
        answer = render_sop_message(capsule, safety_message=safety.message)
        previous_response_id = state.previous_response_id
    else:
        decision = capsule_router.route(
            redaction.redacted_text,
            capsules=capsules,
            active_capsule_id=state.active_for_router(),
            conversation_context=state.context_for_router(),
        )
    if decision.capsule_id == BASELINE_CAPSULE_ID:
        capsule = load_baseline_sop()
        ground_items = []
        ground_warnings = []
        ground_loaded = False
        ground_policy_reason = "baseline SOP has no ground resolution"
        answer, previous_response_id = support_agent.compose(
            redaction.redacted_text,
            capsule,
            ground_items,
            safety_message=safety.message,
            previous_response_id=state.previous_response_id,
        )
    elif decision.capsule_id != CRISIS_SOP_ID:
        capsule = find_capsule(capsules, decision.capsule_id)
        ground_loaded, ground_policy_reason = should_load_ground(
            capsule,
            redaction.redacted_text,
            already_loaded=capsule.get("id", "") in state.grounded_capsule_ids,
        )
        if ground_loaded:
            ground_items, ground_warnings = resolve_ground_with_warnings(capsule)
            state.grounded_capsule_ids.add(capsule.get("id", ""))
        else:
            ground_items = []
            ground_warnings = []
        render_capsule = capsule_for_render(capsule, include_ground=ground_loaded)
        answer, previous_response_id = support_agent.compose(
            redaction.redacted_text,
            render_capsule,
            ground_items,
            safety_message=safety.message,
            previous_response_id=state.previous_response_id,
        )
    guard = guard_output(answer, pii_tags=redaction.tags, safety=safety)

    state.update_after_turn(
        previous_response_id=previous_response_id,
        capsule_id="" if decision.capsule_id in {BASELINE_CAPSULE_ID, CRISIS_SOP_ID} else decision.capsule_id,
        confidence=decision.confidence,
        safety_level=safety.level,
    )
    state.record_turn(
        redacted_user_message=redaction.redacted_text,
        route_id=decision.capsule_id,
        safety_level=safety.level,
    )
    if debug:
        debug_payload = {
            "redaction": redaction.safe_json(),
            "safety": {
                "level": safety.level,
                "reason": safety.reason,
            },
            "route": decision.to_json(),
            "ground": {
                "summary": capsule.get("ground", {}).get("summary", ""),
                "legal_basis_count": len(capsule.get("ground", {}).get("legal_basis", []) or []),
                "practice_basis_count": len(capsule.get("ground", {}).get("practice_basis", []) or []),
                "nodes_count": len(capsule.get("ground", {}).get("nodes", []) or []),
                "loaded": ground_loaded,
                "policy_reason": ground_policy_reason,
                "resolved_ground": [item.ref for item in ground_items],
                "warnings": ground_warnings,
            },
            "output_guard": {
                "passed": guard.passed,
                "warnings": guard.warnings,
            },
            "state": {
                "has_previous_response_id": bool(state.previous_response_id),
                "active_capsule_id": state.active_capsule_id,
                "ttl_turns": state.ttl_turns,
            },
            "capsule_issues": capsule.get("issues", []),
        }
        return (
            guard.text + "\n\n---\nDEBUG\n" + json.dumps(debug_payload, ensure_ascii=False, indent=2),
            state,
        )
    return guard.text, state


def interactive_loop(args: argparse.Namespace) -> None:
    capsules = load_capsules()
    state = ConversationState()
    capsule_router = select_router(offline=args.offline, model=args.model)
    support_agent = select_support_agent(offline=args.offline, model=args.model)
    print("小安 MVP CLI。输入问题开始;输入 /exit 退出。")
    if args.offline:
        print("当前为 offline 模式:不调用 OpenAI,只做本地路由/渲染 smoke test。")
    else:
        print(f"model={get_model(args.model)} api_key={masked_api_key() or '(not set)'}")
    while True:
        try:
            message = input("\n你: ").strip()
        except EOFError:
            print()
            return
        if not message:
            continue
        if message in {"/exit", "/quit"}:
            return
        answer, state = run_turn(
            message,
            capsules,
            state=state,
            model=args.model,
            offline=args.offline,
            debug=args.debug,
            capsule_router=capsule_router,
            support_agent=support_agent,
        )
        print(f"\n小安: {answer}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run XiaoAn capsule+wiki MVP chatflow.")
    parser.add_argument("--once", help="Run one message and exit.")
    parser.add_argument("--model", default="", help="Override configured model for this run.")
    parser.add_argument("--offline", action="store_true", help="Do not call OpenAI; use local smoke-test behavior.")
    parser.add_argument("--debug", action="store_true", help="Print routing and ground debug info.")
    args = parser.parse_args()

    try:
        if args.once:
            capsules = load_capsules()
            capsule_router = select_router(offline=args.offline, model=args.model)
            support_agent = select_support_agent(offline=args.offline, model=args.model)
            answer, _ = run_turn(
                args.once,
                capsules,
                model=args.model,
                offline=args.offline,
                debug=args.debug,
                capsule_router=capsule_router,
                support_agent=support_agent,
            )
            print(answer)
        else:
            interactive_loop(args)
    except (RouterError, GroundResolutionError, ComposeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()
