#!/usr/bin/env bash
# ============================================================
# PangLianTaGeGe Docker 部署辅助脚本
# 用法：bash scripts/docker-deploy.sh <命令>
#    build      构建镜像（backend + frontend）
#    up         启动全部服务（-d 后台）
#    restart    重启全部服务
#    down       停止并移除容器（保留数据卷）
#    logs       跟踪日志
#    ps         查看服务状态
#    init-db    导入数据快照 doc/pangliantagege0402.sql（首次部署用）
#    seed       用示例脚本填充演示数据（populate_db.py / populate_techstack.py）
# ============================================================
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_DIR"

ENV_FILE="docker.env"
if [[ ! -f "$ENV_FILE" ]]; then
  echo "[ERROR] 缺少 $ENV_FILE，请先执行: cp docker.env.example docker.env"
  exit 1
fi

COMPOSE=(docker compose --env-file "$ENV_FILE")

# 确保共享网关网络存在（网关项目创建同名网络，这里兜底）
docker network inspect edge-net >/dev/null 2>&1 || docker network create edge-net

cmd="${1:-up}"

case "$cmd" in
  build)
    "${COMPOSE[@]}" build
    ;;
  up)
    "${COMPOSE[@]}" up -d --build
    "${COMPOSE[@]}" ps
    ;;
  restart)
    "${COMPOSE[@]}" restart
    ;;
  down)
    "${COMPOSE[@]}" down
    ;;
  logs)
    "${COMPOSE[@]}" logs -f --tail=100
    ;;
  ps)
    "${COMPOSE[@]}" ps
    ;;
  init-db)
    # 导入数据快照（表已存在时先 DROP 再重建，内容以快照为准）
    set -a; source "$ENV_FILE"; set +a
    echo "[INFO] 导入数据快照 doc/pangliantagege0402.sql -> ${DB_NAME:-pangliantagege}"
    "${COMPOSE[@]}" exec -T db \
      mysql -uroot -p"${MYSQL_ROOT_PASSWORD:-${DB_PASSWORD:-root}}" "${DB_NAME:-pangliantagege}" \
      < doc/pangliantagege0402.sql
    echo "[OK] 数据导入完成"
    ;;
  seed)
    # 仅建议在空库上执行（populate_techstack 不去重）
    "${COMPOSE[@]}" exec backend python populate_db.py
    "${COMPOSE[@]}" exec backend python populate_techstack.py
    echo "[OK] 演示数据填充完成"
    ;;
  *)
    echo "用法: bash scripts/docker-deploy.sh [build|up|restart|down|logs|ps|init-db|seed]"
    exit 1
    ;;
esac
