#!/bin/bash

# ==========================================
# 配置区域
# ==========================================
# Prod 服务器的 SSH 连接信息 (根据你的 ~/.ssh/config 或实际情况修改)
PROD_SSH="root@8.140.233.55" # 替换为你的服务器 IP 和用户名
# Prod 服务器上 Nginx 配置文件的绝对路径
NGINX_CONF_PATH="/etc/nginx/sites-available/pangliantagege.prod.conf" # 替换为实际路径

# 阿里云安全组配置 (需提前在 Mac 上安装并配置好 aliyun-cli: `brew install aliyun-cli` 然后 `aliyun configure`)
ALIYUN_REGION="cn-beijing" # 请根据实际情况修改地域，例如 cn-hangzhou, cn-shanghai
ALIYUN_SG_ID="sg-2ze77nqw47a1n79qntct"
# 阿里云安全组中专门用于你的 Mac SSH 的规则描述（非常重要，脚本依靠这个描述去找到旧规则并删除）
ALIYUN_SG_RULE_DESC="Macbook_Auto_IP"
# 你需要开放的端口，通常是 SSH(22)，如果还需要别的可以改
TARGET_PORT="22/22" 

# 用于存储上一次 IP 的本地文件
IP_CACHE_FILE="$HOME/.current_mac_ip"

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# 动态生成按天保存的日志文件名 (例如：rag_ip_update_2024-05-20.log)
LOG_FILE="${SCRIPT_DIR}/rag_ip_update_$(date '+%Y-%m-%d').log"

# ==========================================
# 1. 获取当前外网 IP
# ==========================================
# 使用多个国内稳定的源防止获取到代理节点 IP (如梯子节点)
# curl 加上 -m 5 防止超时卡死
CURRENT_IP=$(curl -s -m 5 cip.cc | grep "IP" | awk '{print $3}' | tr -d '\r\n')

if [ -z "$CURRENT_IP" ]; then
    CURRENT_IP=$(curl -s -m 5 https://api.ip.sb/ip | tr -d '\r\n')
fi

if [ -z "$CURRENT_IP" ]; then
    CURRENT_IP=$(curl -s -m 5 https://myip.ipip.net | tr -d '\r\n')
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
    echo "$(date '+%Y-%m-%d %H:%M:%S') - [INFO] IP 未改变 ($CURRENT_IP)，无需更新。" >> "$LOG_FILE"
    exit 0
fi

echo "$(date '+%Y-%m-%d %H:%M:%S') - [INFO] 发现 IP 变化: $OLD_IP -> $CURRENT_IP。开始更新..." >> "$LOG_FILE"

# ==========================================
# 3. 更新阿里云安全组白名单 (放行新 IP 的 SSH 端口)
# ==========================================
if command -v aliyun >/dev/null 2>&1; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - [INFO] 开始更新阿里云安全组 ($ALIYUN_SG_ID)..." >> "$LOG_FILE"
    
    # a. 撤销旧的 IP 授权 (如果有 OLD_IP 的话)
    if [ -n "$OLD_IP" ]; then
        aliyun ecs RevokeSecurityGroup \
            --region "$ALIYUN_REGION" \
            --RegionId "$ALIYUN_REGION" \
            --SecurityGroupId "$ALIYUN_SG_ID" \
            --IpProtocol tcp \
            --PortRange "$TARGET_PORT" \
            --SourceCidrIp "${OLD_IP}/32" >/dev/null 2>&1
        echo "$(date '+%Y-%m-%d %H:%M:%S') - [INFO] 已撤销旧 IP (${OLD_IP}) 的安全组权限。" >> "$LOG_FILE"
    fi

    # b. 添加新的 IP 授权
    AUTH_RESULT=$(aliyun ecs AuthorizeSecurityGroup \
        --region "$ALIYUN_REGION" \
        --RegionId "$ALIYUN_REGION" \
        --SecurityGroupId "$ALIYUN_SG_ID" \
        --IpProtocol tcp \
        --PortRange "$TARGET_PORT" \
        --SourceCidrIp "${CURRENT_IP}/32" \
        --Description "$ALIYUN_SG_RULE_DESC" 2>&1)
        
    if [ $? -eq 0 ]; then
        echo "$(date '+%Y-%m-%d %H:%M:%S') - [SUCCESS] 成功将新 IP (${CURRENT_IP}) 加入安全组白名单。" >> "$LOG_FILE"
    else
        echo "$(date '+%Y-%m-%d %H:%M:%S') - [ERROR] 阿里云安全组更新失败: $AUTH_RESULT" >> "$LOG_FILE"
    fi
    
    # 稍微等待 2 秒让阿里云安全组规则生效
    sleep 2
else
    echo "$(date '+%Y-%m-%d %H:%M:%S') - [WARNING] 未检测到 aliyun-cli 工具，跳过安全组自动更新。如需此功能请先执行 brew install aliyun-cli 并配置。" >> "$LOG_FILE"
fi

# ==========================================
# 4. 通过 SSH 修改 Prod 服务器 Nginx 配置并重启
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