"""DynamoDB-backed multi-turn session manager.

Schema: PK=session_id, SK="state"
TTL field: expires_at (Unix timestamp, 24h)
"""
import time
import uuid
from typing import Any
import boto3
import os
from boto3.dynamodb.conditions import Key


TABLE = os.environ.get("DYNAMODB_TABLE", "xiaoan_sessions")
_db = None


def _table():
    global _db
    if _db is None:
        _db = boto3.resource(
            "dynamodb", region_name=os.environ.get("AWS_REGION", "ap-east-1")
        ).Table(TABLE)
    return _db


def new_session() -> str:
    return str(uuid.uuid4())


def load(session_id: str) -> dict[str, Any]:
    resp = _table().get_item(Key={"session_id": session_id, "sk": "state"})
    return resp.get("Item", {})


def save(session_id: str, state: dict[str, Any]) -> None:
    _table().put_item(
        Item={
            "session_id": session_id,
            "sk": "state",
            "expires_at": int(time.time()) + 86400,
            **state,
        }
    )


def update_after_turn(session_id: str, capsule_id: str | None, response: str, user_msg: str) -> None:
    state = load(session_id)
    history = state.get("history", [])
    history.append({"role": "user", "content": user_msg})
    history.append({"role": "assistant", "content": response})
    # Keep last 10 turns to bound DynamoDB item size
    history = history[-20:]

    new_state = {
        **state,
        "turn_count": state.get("turn_count", 0) + 1,
        "active_capsule_id": capsule_id,
        "ttl_turns": max(0, state.get("ttl_turns", 0) - 1) if capsule_id else 0,
        "history": history,
    }
    save(session_id, new_state)
