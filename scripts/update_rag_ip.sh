#!/bin/bash

# ==========================================
# 配置区域
# ==========================================
# Prod 服务器的 SSH 连接信息 (根据你的 ~/.ssh/config 或实际情况修改)
PROD_SSH="root@8.140.233.55" # 替换为你的服务器 IP 和用户名
# Prod 服务器上 Nginx 配置文件的绝对路径
NGINX_CONF_PATH="/etc/nginx/sites-available/pangliantagege.prod.conf" # 替换为实际路径
# 用于存储上一次 IP 的本地文件
IP_CACHE_FILE="$HOME/.current_mac_ip"

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# 动态生成按天保存的日志文件名 (例如：rag_ip_update_2024-05-20.log)
LOG_FILE="${SCRIPT_DIR}/rag_ip_update_$(date '+%Y-%m-%d').log"

# ==========================================
# 1. 获取当前外网 IP
# ==========================================
# 使用多个源防止某个 API 挂掉
CURRENT_IP=$(curl -s ifconfig.me)
if [ -z "$CURRENT_IP" ]; then
    CURRENT_IP=$(curl -s api.ipify.org)
fi

if [ -z "$CURRENT_IP" ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - [ERROR] 无法获取当前外网 IP。" >> "$LOG_FILE"
    exit 1
fi

# ==========================================
# 2. 对比旧 IP
# ==========================================
OLD_IP=""
if [ -f "$IP_CACHE_FILE" ]; then
    OLD_IP=$(cat "$IP_CACHE_FILE")
fi

if [ "$CURRENT_IP" == "$OLD_IP" ]; then
    # IP 没变，直接退出
    # echo "$(date '+%Y-%m-%d %H:%M:%S') - [INFO] IP 未改变 ($CURRENT_IP)，无需更新。" >> "$LOG_FILE"
    exit 0
fi

echo "$(date '+%Y-%m-%d %H:%M:%S') - [INFO] 发现 IP 变化: $OLD_IP -> $CURRENT_IP。开始更新 Prod 服务器..." >> "$LOG_FILE"

# ==========================================
# 3. 通过 SSH 修改 Prod 服务器 Nginx 配置并重启
# ==========================================
# 使用 sed 命令：找到包含 RAG_MAC_IP_MARKER 的这一行，将其替换为新的 proxy_pass 语句
# 注意：如果不是 root 登录，sed 前面可能需要加 sudo
SSH_CMD="sudo sed -i 's|proxy_pass http://.*:8001; # RAG_MAC_IP_MARKER|proxy_pass http://${CURRENT_IP}:8001; # RAG_MAC_IP_MARKER|' ${NGINX_CONF_PATH} && sudo nginx -t && sudo nginx -s reload"

# 执行远程命令
ssh -o StrictHostKeyChecking=no "$PROD_SSH" "$SSH_CMD"

if [ $? -eq 0 ]; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - [SUCCESS] Prod 服务器 Nginx 更新成功，新 IP: $CURRENT_IP" >> "$LOG_FILE"
    # 更新本地缓存
    echo "$CURRENT_IP" > "$IP_CACHE_FILE"
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - [ERROR] Prod 服务器更新失败，请检查 SSH 连接或权限。" >> "$LOG_FILE"
fi