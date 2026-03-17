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
  
  # Collect static files for Django admin
  pushd "$DEST_DIR/backend" >/dev/null
  python manage.py collectstatic --noinput
  popd >/dev/null
  
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

    # Static files from Django (Admin CSS/JS)
    location /static/ {
        alias /var/pltgg/backend/staticfiles/;
        access_log off;
        expires 30d;
    }

    # Proxy API and Admin to Django dev server
    location ~ ^/(api|admin)/ {
        proxy_pass http://127.0.0.1:8000;
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
  echo "Configuring and restarting systemd services..."
  
  # Copy service files to /etc/systemd/system/
  cp "$DEST_DIR/plapi.service" /etc/systemd/system/
  cp "$DEST_DIR/plui.service" /etc/systemd/system/

  # Reload systemd to pick up new files
  systemctl daemon-reload

  # Check for MySQL service
  local db_engine_env=""
  if systemctl is-active --quiet mysql; then
    echo "MySQL service detected. Using MySQL."
  else
    echo "MySQL service NOT detected. Switching to SQLite for backend."
    # We need to inject this into the service file or override it
    # For simplicity, let's create a drop-in override if needed, or just sed the file before copy
    # But since we already copied, let's use systemctl edit mechanism or just modify the file in place
    if ! grep -q "DB_ENGINE=sqlite3" /etc/systemd/system/plapi.service; then
        # Add Environment variable to [Service] section
        sed -i '/^Environment="ALLOWED_HOSTS=\*"/a Environment="DB_ENGINE=sqlite3"' /etc/systemd/system/plapi.service
        systemctl daemon-reload
    fi
  fi

  # Enable and restart services
  systemctl enable plapi
  systemctl enable plui
  
  echo "Restarting plapi (Backend)..."
  systemctl restart plapi
  
  echo "Restarting plui (Frontend)..."
  systemctl restart plui
}

set_permissions() {
  chown -R www-data:www-data "$DEST_DIR"
}

configure_firewall() {
  if command -v ufw >/dev/null 2>&1; then
    if ufw status | grep -q "Status: active"; then
      echo "Configuring UFW firewall..."
      ufw allow 80/tcp
      ufw allow 8000/tcp
      ufw allow 5173/tcp
      ufw reload
    fi
  fi
}

check_services() {
  echo "Checking services..."
  sleep 3
  if systemctl is-active --quiet plapi; then
    echo "Backend (plapi) is running."
  else
    echo "WARNING: Backend failed to start. Check 'journalctl -u plapi'"
  fi
  
  if systemctl is-active --quiet plui; then
    echo "Frontend (plui) is running."
  else
    echo "WARNING: Frontend failed to start. Check 'journalctl -u plui'"
  fi
}

main() {
  ensure_root "$@"
  install_basics
  copy_code
  setup_python
  setup_node
  write_nginx_conf
  set_permissions
  configure_firewall
  restart_services
  check_services
  
  # Get IP address
  IP=$(hostname -I | awk '{print $1}')
  echo "-----------------------------------------------------"
  echo "Deploy finished."
  echo "Nginx (Production): http://$IP/"
  echo "Frontend (Preview): http://$IP:5173/"
  echo "Backend API:        http://$IP:8000/"
  echo "-----------------------------------------------------"
}

main "$@"

