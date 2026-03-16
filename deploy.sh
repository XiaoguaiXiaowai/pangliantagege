#!/usr/bin/env bash
set -euo pipefail

# Deploy script for Ubuntu 24.04
# - Copies code to /var/pltgg
# - Installs backend (Python) and frontend (Node) dependencies
# - Builds frontend
# - Configures nginx
# - Starts/restarts backend and frontend in background

DEST_DIR="/var/pltgg"
NGINX_AVAIL="/etc/nginx/sites-available"
NGINX_ENABLED="/etc/nginx/sites-enabled"
SITE_NAME="kubeset.conf"

ensure_root() {
  if [[ "$EUID" -ne 0 ]]; then
    echo "Re-running with sudo..."
    exec sudo -E bash "$0" "$@"
  fi
}

install_basics() {
  apt-get update
  # nodejs from NodeSource includes npm, so we don't need to install npm separately
  DEBIAN_FRONTEND=noninteractive apt-get install -y rsync python3-venv python3-pip nginx nodejs
}

copy_code() {
  mkdir -p "$DEST_DIR"
  rsync -a --delete \
    --exclude ".git" \
    --exclude ".venv" \
    --exclude "venv" \
    --exclude "__pycache__" \
    --exclude "frontend/node_modules" \
    "$(pwd)/" "$DEST_DIR/"
}

setup_python() {
  local venv_dir="$DEST_DIR/backend/venv"
  python3 -m venv "$venv_dir"
  # shellcheck disable=SC1090
  source "$venv_dir/bin/activate"
  pip install -U pip wheel
  pip install -r "$DEST_DIR/backend/requirements.txt"
  deactivate
}

setup_node() {
  pushd "$DEST_DIR/frontend" >/dev/null
  npm ci || npm install
  npm run build
  popd >/dev/null
}

write_nginx_conf() {
  cat > "$NGINX_AVAIL/$SITE_NAME" <<'EOF'
server {
    listen 80;
    server_name _;

    # Serve built frontend
    root /var/pltgg/frontend/dist;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    # Static media from Django
    location /media/ {
        alias /var/pltgg/backend/media/;
        access_log off;
        expires 30d;
    }

    # Proxy API to Django dev server
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

  ln -sf "$NGINX_AVAIL/$SITE_NAME" "$NGINX_ENABLED/$SITE_NAME"
  # Optionally disable default site
  if [[ -e "$NGINX_ENABLED/default" ]]; then
    rm -f "$NGINX_ENABLED/default"
  fi
  nginx -t
  systemctl reload nginx
}

restart_services() {
  pushd "$DEST_DIR" >/dev/null
  mkdir -p logs run
  # Stop if running
  python3 stop_backend.py || true
  python3 stop_frontend.py || true
  # Start
  ALLOWED_HOSTS="*" DJANGO_DEBUG=false python3 start_backend.py
  sleep 1
  python3 start_frontend.py
  popd >/dev/null
}

set_permissions() {
  chown -R www-data:www-data "$DEST_DIR"
}

main() {
  ensure_root "$@"
  install_basics
  copy_code
  setup_python
  setup_node
  write_nginx_conf
  set_permissions
  restart_services
  echo "Deploy finished. Site served by nginx and background processes."
}

main "$@"

