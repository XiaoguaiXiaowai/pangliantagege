#!/usr/bin/env bash
set -euo pipefail

# Deploy script for Ubuntu 24.04
# Usage: sudo bash deploy.sh [stg|prod]
# Default is stg if no argument provided.

ENV=${1:-stg}

DEST_DIR="/var/pltgg"
NGINX_AVAIL="/etc/nginx/sites-available"
NGINX_ENABLED="/etc/nginx/sites-enabled"

if [[ "$ENV" == "prod" ]]; then
  SITE_NAME="pangliantagege.prod.conf"
  DOMAIN="www.pangliantagege.top"
  echo "Deploying to PRODUCTION environment ($DOMAIN)"
else
  SITE_NAME="pangliantagege.conf"
  DOMAIN="stg.pangliantagege.com"
  echo "Deploying to STAGING environment ($DOMAIN)"
fi

ensure_root() {
  if [[ "$EUID" -ne 0 ]]; then
    echo "Re-running with sudo..."
    exec sudo -E bash "$0" "$@"
  fi
}

install_basics() {
  apt-get update
  
  # Install prerequisites for NodeSource
  DEBIAN_FRONTEND=noninteractive apt-get install -y ca-certificates curl gnupg
  
  # Setup NodeSource repository for Node.js 22
  mkdir -p /etc/apt/keyrings
  curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg --yes
  echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_22.x nodistro main" > /etc/apt/sources.list.d/nodesource.list
  
  apt-get update
  
  # Install build dependencies and Node.js
  DEBIAN_FRONTEND=noninteractive apt-get install -y \
    rsync python3-venv python3-pip nginx nodejs \
    libjpeg-dev zlib1g-dev libpng-dev libfreetype6-dev \
    libssl-dev libffi-dev python3-dev pkg-config build-essential
    
  # Upgrade npm to latest version to support modern package.json features (like aliases)
  npm install -g npm@latest
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
    
  # Create media directory if it doesn't exist
  mkdir -p "$DEST_DIR/backend/media"
  
  # Copy SSL certs if they exist and we are in PROD
  if [[ "$ENV" == "prod" ]]; then
    mkdir -p "$DEST_DIR/https"
    if [[ -d "$(pwd)/https" ]]; then
      cp -r "$(pwd)/https/"* "$DEST_DIR/https/"
      # Set permissions for certs (readable by root/nginx)
      chmod 600 "$DEST_DIR/https/"*.key
      chmod 644 "$DEST_DIR/https/"*.pem
    fi
  fi
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
  # Remove node_modules and package-lock.json to ensure clean install if needed
  rm -rf node_modules package-lock.json
  
  # Use npm install instead of npm ci to be more forgiving about lockfile issues
  npm install --legacy-peer-deps
  npm run build
  popd >/dev/null
}

write_nginx_conf() {
  # Base config content
  cat > "$NGINX_AVAIL/$SITE_NAME" <<EOF
server {
EOF

  # SSL Configuration for PROD
  if [[ "$ENV" == "prod" ]]; then
    cat >> "$NGINX_AVAIL/$SITE_NAME" <<EOF
    listen 80;
    server_name $DOMAIN;
    return 301 https://\$host\$request_uri;
}

# Redirect non-www apex to www (HTTP)
server {
    listen 80;
    server_name pangliantagege.top;
    return 301 https://www.pangliantagege.top\$request_uri;
}

server {
    listen 443 ssl;
    server_name $DOMAIN;

    ssl_certificate /var/pltgg/https/${DOMAIN}.pem;
    ssl_certificate_key /var/pltgg/https/${DOMAIN}.key;
    
    # Recommended SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
EOF

    # Optional: HTTPS redirect for apex domain if cert present
    if [[ -f "/var/pltgg/https/pangliantagege.top.pem" && -f "/var/pltgg/https/pangliantagege.top.key" ]]; then
      cat >> "$NGINX_AVAIL/$SITE_NAME" <<'EOF'
server {
    listen 443 ssl;
    server_name pangliantagege.top;

    ssl_certificate /var/pltgg/https/pangliantagege.top.pem;
    ssl_certificate_key /var/pltgg/https/pangliantagege.top.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    return 301 https://www.pangliantagege.top$request_uri;
}
EOF
    else
      echo "NOTE: HTTPS cert for apex domain (pangliantagege.top) not found. HTTPS redirect for apex will not work until cert is provided."
    fi
  else
    # Non-SSL config for STG
    cat >> "$NGINX_AVAIL/$SITE_NAME" <<EOF
    listen 80;
    server_name $DOMAIN;
EOF
  fi

  # Common config (Locations)
  cat >> "$NGINX_AVAIL/$SITE_NAME" <<EOF
    
    # Increase body size limit to 20M to allow larger image uploads
    client_max_body_size 20M;

    # Serve built frontend
    root /var/pltgg/frontend/dist;
    index index.html;

    # Static media from Django
    location /media/ {
        alias /var/pltgg/backend/media/;
        autoindex off;
        access_log off;
        expires 30d;
        add_header Cache-Control "public";
    }

    # Static files from Django (Admin CSS/JS)
    location /static/ {
        alias /var/pltgg/backend/staticfiles/;
        access_log off;
        expires 30d;
    }

    # Proxy API and Admin to Django dev server
    # Important: Admin URLs are dynamic, so they must be proxied
    # But /static/admin/ is served by the static location block above
    location ~ ^/(api|admin)/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    # Frontend catch-all (for SPA)
    # Must be last or have lower priority than specific locations
    location / {
        try_files \$uri \$uri/ /index.html;
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

  # Inject CSRF_TRUSTED_ORIGINS into plapi.service
  sed -i '/^Environment="ALLOWED_HOSTS=\*"/a Environment="CSRF_TRUSTED_ORIGINS=https://'"$DOMAIN"'"' /etc/systemd/system/plapi.service

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
    fi
  fi
  
  # Inject CSRF_TRUSTED_ORIGINS into plapi.service (always needed for HTTPS)
  # Remove old entry if exists to avoid duplicates
  sed -i '/CSRF_TRUSTED_ORIGINS/d' /etc/systemd/system/plapi.service
  sed -i '/^Environment="ALLOWED_HOSTS=\*"/a Environment="CSRF_TRUSTED_ORIGINS=https://'"$DOMAIN"'"' /etc/systemd/system/plapi.service
  
  systemctl daemon-reload
  systemctl enable plapi
  systemctl enable plui
  
  echo "Restarting plapi (Backend)..."
  systemctl restart plapi
  
  echo "Restarting plui (Frontend)..."
  systemctl restart plui
}

set_permissions() {
  chown -R www-data:www-data "$DEST_DIR"
  # Ensure media directory is writable
  chmod -R 775 "$DEST_DIR/backend/media"
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
  echo "Deploy finished for $ENV environment."
  echo "Domain:             http://$DOMAIN/"
  echo "Nginx (Production): http://$IP/"
  echo "Frontend (Preview): http://$IP:5173/"
  echo "Backend API:        http://$IP:8000/"
  echo "-----------------------------------------------------"
}

main "$@"
