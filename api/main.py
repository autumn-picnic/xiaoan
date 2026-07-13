"""FastAPI entry point — /chat REST API with Vercel frontend CORS."""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

from chatflow.pipeline import run as pipeline_run

app = FastAPI(title="XiaoAn Chatflow")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.environ.get("VERCEL_ORIGIN", "*")],
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    session_id: str = ""
    message: str


class ChatResponse(BaseModel):
    session_id: str
    response: str
    debug: dict = {}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    response, session_id, debug = pipeline_run(req.session_id, req.message)
    return ChatResponse(session_id=session_id, response=response, debug=debug)


@app.get("/health")
async def health():
    return {"status": "ok"}
