from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class ConversationState:
    previous_response_id: str = ""
    active_capsule_id: str = ""
    ttl_turns: int = 0
    safety_level: str = "normal"
    recent_turns: list[dict[str, str]] = field(default_factory=list)
    grounded_capsule_ids: set[str] = field(default_factory=set)

    def active_for_router(self) -> str:
        return self.active_capsule_id if self.ttl_turns > 0 else ""

    def context_for_router(self, limit: int = 6) -> list[dict[str, str]]:
        return self.recent_turns[-limit:]

    def record_turn(self, *, redacted_user_message: str, route_id: str, safety_level: str) -> None:
        self.recent_turns.append(
            {
                "user": redacted_user_message,
                "route_id": route_id,
                "safety_level": safety_level,
            }
        )
        self.recent_turns = self.recent_turns[-12:]

    def update_after_turn(
        self,
        *,
        previous_response_id: str = "",
        capsule_id: str = "",
        confidence: float = 0.0,
        safety_level: str = "normal",
    ) -> None:
        self.previous_response_id = previous_response_id or self.previous_response_id
        self.safety_level = safety_level
        if safety_level != "normal":
            self.active_capsule_id = ""
            self.ttl_turns = 0
            self.grounded_capsule_ids.clear()
            return
        if capsule_id and confidence >= 0.45:
            self.active_capsule_id = capsule_id
            self.ttl_turns = 3
        elif self.ttl_turns > 0:
            self.ttl_turns -= 1
