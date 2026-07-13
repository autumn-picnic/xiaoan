#!/usr/bin/env bash
# EC2 setup and launch script (Ubuntu 22.04, run as root)
set -euo pipefail

PROJECT_DIR="/opt/xiaoan"
ENV_FILE="$PROJECT_DIR/.env"

# --- System deps ---
apt-get update -q
apt-get install -y python3-venv python3-pip nginx certbot python3-certbot-nginx

# --- Project ---
mkdir -p "$PROJECT_DIR"
cp -r . "$PROJECT_DIR/"
cd "$PROJECT_DIR"

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# --- .env (edit values before running) ---
cat > "$ENV_FILE" <<'EOF'
AZURE_OPENAI_KEY=your_azure_openai_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AWS_REGION=ap-east-1
S3_BUCKET=your-xiaoan-bucket
DYNAMODB_TABLE=xiaoan_sessions
WECHAT_TOKEN=your_wechat_token
EOF
chmod 600 "$ENV_FILE"

# --- GraphRAG index ---
echo "Running GraphRAG indexing (30-60 min)..."
source "$ENV_FILE" && python scripts/01_setup_graphrag.py && python scripts/02_index_graphrag.py

# --- Systemd service ---
cat > /etc/systemd/system/xiaoan.service <<EOF
[Unit]
Description=XiaoAn Chatflow API
After=network.target

[Service]
User=ubuntu
WorkingDirectory=$PROJECT_DIR
EnvironmentFile=$ENV_FILE
ExecStart=$PROJECT_DIR/.venv/bin/uvicorn api.main:app --host 127.0.0.1 --port 8000
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

systemctl enable xiaoan
systemctl start xiaoan

# --- Nginx reverse proxy ---
cat > /etc/nginx/sites-available/xiaoan <<'NGINX'
server {
    listen 80;
    server_name _;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
NGINX
ln -sf /etc/nginx/sites-available/xiaoan /etc/nginx/sites-enabled/
nginx -t && systemctl reload nginx

echo ""
echo "Done. Update AZURE_OPENAI_KEY / WECHAT_TOKEN in $ENV_FILE, then:"
echo "  systemctl restart xiaoan"
echo "For HTTPS (required for WeChat): certbot --nginx -d your.domain.com"
