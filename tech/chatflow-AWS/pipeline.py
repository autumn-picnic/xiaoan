"""XiaoAn chatflow pipeline — runs the 5-stage architecture.md flow inline on EC2.

Stage order: PII → Safety → [Crisis?] → Retrieval → Agent → Guard
"""
from chatflow.stages import pii, safety, retrieval, agent, guard
from chatflow import session as sess


def run(session_id: str, user_input: str) -> tuple[str, str, dict]:
    """Execute one conversational turn. Returns (response, session_id, debug)."""
    if not session_id:
        session_id = sess.new_session()

    session_state = sess.load(session_id)

    state = {
        "user_input": user_input,
        "session_id": session_id,
        "session_state": session_state,
    }

    state = pii.run(state)
    state = safety.run(state)

    if state["red_flag"]:
        state = agent.run(state)
        state = guard.run(state)
    else:
        state = retrieval.run(state)
        state = agent.run(state)
        state = guard.run(state)

    response = state["response"]
    sess.update_after_turn(session_id, state.get("capsule_id"), response, user_input)

    debug = {
        "capsule_id": state.get("capsule_id"),
        "retrieval_score": state.get("retrieval_score"),
        "red_flag": state.get("red_flag", False),
    }
    return response, session_id, debug
