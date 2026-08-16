#!/usr/bin/env bash
# ============================================================
# 生产服务器部署脚本（由 GitHub Actions 通过受限 SSH 调用）
# 部署位置: /opt/git/pltgg/scripts/remote-deploy.sh
#
# 职责：
#   1. 从 GitHub 同步代码（public 仓库，https 免密 fetch）
#   2. 拉取最新镜像（ghcr.io）
#   3. 重建 backend / frontend 容器（容器内自动 migrate + collectstatic）
#   4. 清理旧镜像
#
# 注意：git reset --hard 会丢弃 /opt/git/pltgg 下所有未提交改动，
#       请勿在该目录手动修改文件（docker.env / backend/media 不受影响，已 gitignore）
# ============================================================
set -euo pipefail

REPO_DIR="/opt/git/pltgg"
GITHUB_URL="https://github.com/XiaoguaiXiaowai/pangliantagege.git"
GITHUB_BRANCH="master"

cd "$REPO_DIR"

echo "[1/4] 同步代码 (GitHub ${GITHUB_BRANCH})..."
git fetch "$GITHUB_URL" "$GITHUB_BRANCH:refs/remotes/github/master"
git reset --hard "github/master"
git log --oneline -1

echo "[2/4] 拉取最新镜像 (ghcr.io)..."
docker compose --env-file docker.env pull backend frontend

echo "[3/4] 重建容器..."
docker compose --env-file docker.env up -d --force-recreate backend frontend

echo "[4/4] 清理旧镜像..."
docker image prune -f >/dev/null 2>&1 || true

echo "✅ 部署完成: $(date '+%F %T %Z')"
docker compose --env-file docker.env ps --format 'table {{.Name}}\t{{.Status}}'
