"""GraphRAG local search for capsule retrieval."""
import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from graphrag.query.cli import run_local_search

WORKSPACE = Path(__file__).parent.parent.parent / "graphrag_workspace"

_SHIFT_SIGNALS = ["换个话题", "另外", "我想问", "不是这个"]


def run(state: dict) -> dict:
    text = state.get("redacted_input", state["user_input"])
    session_state = state.get("session_state", {})
    active_capsule_id = session_state.get("active_capsule_id")
    ttl_turns = session_state.get("ttl_turns", 0)

    if active_capsule_id and ttl_turns > 0 and not _is_topic_shift(text):
        return {**state, "capsule_found": True, "capsule_id": active_capsule_id,
                "retrieval_result": session_state.get("last_retrieval", ""), "retrieval_score": 1.0}

    result = _local_query(text)
    capsule_found = bool(result and len(result.strip()) > 50)

    return {
        **state,
        "capsule_found": capsule_found,
        "capsule_id": "retrieved" if capsule_found else None,
        "retrieval_result": result,
        "retrieval_score": 1.0 if capsule_found else 0.0,
    }


def _local_query(query: str) -> str:
    with ThreadPoolExecutor(max_workers=1) as executor:
        future = executor.submit(_run_graphrag, query)
        return future.result()


def _run_graphrag(query: str) -> str:
    return run_local_search(
        root_dir=str(WORKSPACE),
        config_filepath=None,
        data_dir=str(WORKSPACE / "output"),
        community_level=2,
        response_type="single paragraph",
        streaming=False,
        query=query,
    )


def _is_topic_shift(text: str) -> bool:
    return any(sig in text for sig in _SHIFT_SIGNALS)
