from __future__ import annotations

from dataclasses import dataclass


# POC stub: interface only. Real PII redaction is a production concern and is
# intentionally not implemented here. redact_pii passes text through unchanged
# so the rest of the pipeline (router/compose/output_guard) keeps its seam.


@dataclass
class PiiTag:
    type: str
    placeholder: str
    value: str

    def safe_json(self) -> dict[str, str]:
        return {"type": self.type, "placeholder": self.placeholder}


@dataclass
class RedactionResult:
    redacted_text: str
    tags: list[PiiTag]

    def safe_json(self) -> dict[str, object]:
        return {
            "redacted_text": self.redacted_text,
            "pii_tags": [tag.safe_json() for tag in self.tags],
        }


def redact_pii(raw_text: str) -> RedactionResult:
    return RedactionResult(redacted_text=raw_text, tags=[])
