#!/usr/bin/env bash
# ============================================================
# GitHub Actions 部署密钥 SSH 门卫
# 部署位置: /opt/git/pltgg/scripts/ssh-gate.sh
# 配合 authorized_keys 的 command="..." 使用：
#
#   command="/opt/git/pltgg/scripts/ssh-gate.sh",restrict \
#     ssh-ed25519 AAAA... github-actions-deploy
#
# 该密钥只能做两件事：
#   1. git 推送/拉取到 /opt/git/pltgg.git（git-receive-pack / git-upload-pack）
#   2. 执行部署脚本 remote-deploy.sh（无参数 SSH 时）
# 无法打开交互 shell，无法执行其他命令 —— 即使 GitHub 密钥泄露也无法登录服务器。
# ============================================================
set -euo pipefail

GIT_REPO="/opt/git/pltgg.git"
DEPLOY_SCRIPT="/opt/git/pltgg/scripts/remote-deploy.sh"

case "${SSH_ORIGINAL_COMMAND:-}" in
  # git push / git pull（客户端发来的命令带引号路径，这里精确匹配两种形式）
  "git-receive-pack '/opt/git/pltgg.git'"|"git-receive-pack /opt/git/pltgg.git")
    exec git-receive-pack "$GIT_REPO"
    ;;
  "git-upload-pack '/opt/git/pltgg.git'"|"git-upload-pack /opt/git/pltgg.git")
    exec git-upload-pack "$GIT_REPO"
    ;;
  *)
    # 其他一切请求（含无命令的纯 SSH）→ 执行部署脚本
    exec "$DEPLOY_SCRIPT"
    ;;
esac
