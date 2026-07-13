"""Main LLM stage: capsule render or baseline SOP via Azure OpenAI."""
import os
from openai import OpenAI

_client = None


def _llm() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(
            api_key=os.environ["AZURE_OPENAI_KEY"],
            base_url=os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/"),
        )
    return _client


_CRISIS_SOP = """你现在处理的是家暴紧急情况。
请立即告知用户：
1. 如处于危险，拨打110报警
2. 全国家暴热线：400-779-9995
3. 可以离开现场到安全地点
保持语气冷静、清晰、不评判。"""

_BASELINE_SYSTEM = """你是小安，专注家暴支持的AI助手。
遵循RAG原则：Recognize（共情）→ Act（行动步骤）→ Ground（法律依据）。
回应要温暖、具体、可操作。不超过300字。"""


def run(state: dict) -> dict:
    if state.get("red_flag"):
        return {**state, "response": _crisis_response(state)}

    history = state.get("session_state", {}).get("history", [])
    context = state.get("retrieval_result", "")
    capsule_found = state.get("capsule_found", False)

    system = _BASELINE_SYSTEM
    if capsule_found and context:
        system += f"\n\n以下是相关场景指引，请据此回答：\n{context[:2000]}"

    messages = [{"role": "system", "content": system}]
    messages += history[-6:]  # last 3 turns for context
    messages.append({"role": "user", "content": state.get("redacted_input", state["user_input"])})

    resp = _llm().responses.create(model="gpt-5-mini", input=messages)
    content = resp.output_text or ""
    return {**state, "response": content}


def _crisis_response(state: dict) -> str:
    resp = _llm().responses.create(
        model="gpt-5-mini",
        input=[
            {"role": "system", "content": _CRISIS_SOP},
            {"role": "user", "content": state.get("redacted_input", state["user_input"])},
        ],
    )
    return resp.output_text or ""
