# XiaoAn Deployment — Next Steps

## Blocker: GraphRAG 索引失敗

**問題**：`ValueError: Columns must be same length as key` 在 entity summarization 步驟
**根本原因**：Capsule 文件的 YAML frontmatter 格式不一致，graphrag LLM 抽取 entity 時返回不一致的欄位數，導致 pandas 無法合併
**現狀**：retrieval.py 已還原為 graphrag local_search，但 EC2 上部署的是 embedding fallback 版本（可用但召回率低）

---

## 待辦事項

### 1. 統一 Capsule YAML Frontmatter 格式 [必做，阻塞 graphrag]
- 確認所有 `capsule/*.md` 有相同的必填欄位（`title`, `status`, `triggers` 等）
- 移除缺失或多餘的 YAML 鍵值
- 特別檢查：`N3a_報警.md` 和 `N3a_ 報警.md`（重複 capsule）
- 完成後重新跑 `python scripts/01_setup_graphrag.py && python scripts/02_index_graphrag.py` on EC2

### 2. 驗證 GraphRAG 索引完整性 [完成 #1 後]
```bash
find /opt/xiaoan/graphrag_workspace/output -name "create_final_nodes.parquet"
```
需要看到這個文件才算索引成功

### 3. 部署新 retrieval.py [完成 #2 後]
```bash
rsync -avz -e "ssh -i ~/Downloads/xiaoan.pem" \
  /Users/mingjiexing/Desktop/ADVchatbot/xiaoan/chatflow/ \
  ubuntu@34.227.103.81:/opt/xiaoan/chatflow/
```
然後 `pkill -f uvicorn && bash /opt/xiaoan/start.sh`

### 4. 連接 Vercel 前端 (anti-dv.vercel.app) [可立即做]
- EC2 CORS 已設定為 `https://anti-dv.vercel.app` ✓
- **問題**：Vercel(HTTPS) 呼叫 EC2 (HTTP port 8000) 會觸發瀏覽器 Mixed Content 錯誤
- **解法**：EC2 需要 HTTPS。需要一個域名 + Let's Encrypt SSL：
  ```bash
  sudo certbot --nginx -d your.domain.com
  ```
  或用 CloudFront / Nginx SSL termination

### 5. 建立黃金測試集 [可立即做]
| 輸入 | 期待 capsule |
|---|---|
| "我不確定這算不算家暴" | N1 識別暴力 |
| "警察說是家務事不管" | N3a 報警 |
| "如何申請保護令" | N5p 人身安全保護令 |
| "他拿刀威脅我" | Crisis SOP |

### 6. Systemd 開機自啟 [上線前]
```bash
sudo systemctl enable xiaoan
```

---

## 現有部署狀態

| 項目 | 狀態 |
|---|---|
| EC2 API (port 8000) | ✅ 運行中 (embedding retrieval) |
| DynamoDB session 管理 | ✅ |
| Azure OpenAI gpt-5-mini | ✅ |
| GraphRAG local search | ❌ 等待 capsule 格式統一 |
| HTTPS / 域名 | ❌ 待設定 |
| Vercel 前端連接 | ❌ 需要 HTTPS 先 |
