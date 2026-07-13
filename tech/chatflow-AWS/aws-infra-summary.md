# XiaoAn AWS Infrastructure 概覽

## 計算

- EC2 `t3.micro`（免費層），Ubuntu 24.04 LTS
- IP：`34.227.103.81`，region：`us-east-1`
- 跑 FastAPI (uvicorn, port 8000)，用 `start.sh` 啟動

## 儲存

- DynamoDB table `xiaoan_sessions`：存對話 session
- S3 bucket `xiaoan-chatflow-try`：存 chatflow 相關檔案

## LLM

- Azure OpenAI（`xiaoanautumn.openai.azure.com`），模型 `gpt-5-mini`
- Embedding：`text-embedding-3-small`
- 檢索走 cosine similarity（threshold 0.45），graphrag 有裝但未啟用（index 不完整）

## 已知問題與建議

1. **單點故障**：只有一台 EC2，沒有 load balancer 或 auto-scaling。instance 掛了服務就停。
2. **t3.micro 限制**：1 vCPU / 1GB RAM，embedding 計算量大時可能成為瓶頸。
3. **graphrag 裝而不用**：index 因 pandas 錯誤不完整，RAG 品質受限於純 cosine similarity，下個階段值得處理。

## 啟動指令（EC2）

```bash
cd /opt/xiaoan && bash start.sh
# start.sh: set -a && source .env && set +a && uvicorn api.main:app --host 0.0.0.0 --port 8000 --loop asyncio
```
