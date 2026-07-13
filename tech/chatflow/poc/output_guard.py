from __future__ import annotations

from dataclasses import dataclass

from pii_redactor import PiiTag
from safety import SafetySignal


# POC stub: interface only. The output guard (re-redaction, overpromise
# detection, internal-term leak detection, red-flag injection) is a production
# concern and is intentionally not implemented here. guard_output returns the
# answer unchanged so the pipeline keeps its seam.


@dataclass
class GuardResult:
    passed: bool
    warnings: list[str]
    text: str


def guard_output(answer: str, *, pii_tags: list[PiiTag], safety: SafetySignal) -> GuardResult:
    return GuardResult(passed=True, warnings=[], text=answer)
