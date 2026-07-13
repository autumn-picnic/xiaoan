"""Run GraphRAG indexing and upload artifacts to S3."""
import asyncio
import os
import boto3
from pathlib import Path
from dotenv import load_dotenv
from graphrag.index import run_pipeline_with_config

load_dotenv()

ROOT = Path(__file__).parent.parent
WORKSPACE = ROOT / "graphrag_workspace"


def index():
    print("Running GraphRAG indexing (this may take 30-60 minutes)...")
    asyncio.run(_run())
    print("Indexing complete.")
    _upload_to_s3()


async def _run():
    from graphrag.config import load_config
    from graphrag.index import create_pipeline_config
    graphrag_config = load_config(root_dir=str(WORKSPACE))
    pipeline_config = create_pipeline_config(graphrag_config)
    async for result in run_pipeline_with_config(pipeline_config):
        if result.errors:
            print(f"Error: {result.errors}")


def _upload_to_s3():
    bucket = os.environ["S3_BUCKET"]
    s3 = boto3.client("s3", region_name=os.environ.get("AWS_REGION", "us-east-1"))
    output_dir = WORKSPACE / "output"

    uploaded = 0
    for f in output_dir.rglob("*"):
        if f.is_file():
            key = f"graphrag/{f.relative_to(output_dir)}"
            s3.upload_file(str(f), bucket, key)
            uploaded += 1

    print(f"Uploaded {uploaded} artifacts to s3://{bucket}/graphrag/")


if __name__ == "__main__":
    index()

