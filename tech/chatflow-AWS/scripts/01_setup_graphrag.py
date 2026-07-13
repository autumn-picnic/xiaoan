"""Initialize GraphRAG workspace and write settings.yaml with Azure OpenAI config."""
import os
import re
import shutil
import yaml
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).parent.parent
WORKSPACE = ROOT / "graphrag_workspace"
INPUT_DIR = WORKSPACE / "input"


def _strip_frontmatter(text: str) -> str:
    if text.startswith("---"):
        match = re.match(r'^---\n.*?\n---\n', text, re.DOTALL)
        if match:
            return text[match.end():].strip()
    return text.strip()


def setup():
    if WORKSPACE.exists():
        shutil.rmtree(WORKSPACE)

    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    for src in [ROOT / "capsule", ROOT / "knowledge" / "wiki"]:
        for f in src.rglob("*.md"):
            text = _strip_frontmatter(f.read_text(encoding="utf-8"))
            if len(text) > 50:  # skip nearly-empty files
                dest = INPUT_DIR / f"{src.name}_{f.name}"
                dest.write_text(text, encoding="utf-8")

    endpoint = os.environ["AZURE_OPENAI_ENDPOINT"].rstrip("/")

    settings = {
        "llm": {
            "api_key": os.environ["AZURE_OPENAI_KEY"],
            "type": "openai_chat",
            "model": "gpt-5-mini",
            "api_base": endpoint,
            "max_tokens": 2000,
        },
        "embeddings": {
            "llm": {
                "api_key": os.environ["AZURE_OPENAI_KEY"],
                "type": "openai_embedding",
                "model": "text-embedding-3-small",
                "api_base": endpoint,
            }
        },
        "input": {
            "type": "file",
            "file_type": "text",
            "base_dir": str(INPUT_DIR),
            "file_encoding": "utf-8",
            "file_pattern": ".*\\.md$",
        },
        "storage": {
            "type": "file",
            "base_dir": str(WORKSPACE / "output"),
        },
        "encoding_model": "cl100k_base",
        "skip_workflows": [],
    }

    with open(WORKSPACE / "settings.yaml", "w", encoding="utf-8") as f:
        yaml.dump(settings, f, allow_unicode=True, default_flow_style=False)

    print(f"GraphRAG workspace initialized at {WORKSPACE}")
    print(f"Input files: {len(list(INPUT_DIR.glob('*.md')))} markdown files")


if __name__ == "__main__":
    setup()
