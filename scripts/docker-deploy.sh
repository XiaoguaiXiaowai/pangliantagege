#!/usr/bin/env bash
# ============================================================
# PangLianTaGeGe Docker 部署辅助脚本
# 用法：bash scripts/docker-deploy.sh <命令>
#    build      构建镜像（backend + frontend）
#    up         启动全部服务（-d 后台）— 启动前自动执行数据库迁移
#    restart    重启全部服务 — 重启前自动执行数据库迁移
#    down       停止并移除容器（保留数据卷）
#    logs       跟踪日志
#    ps         查看服务状态
#    migrate    手动执行数据库迁移（先 up db，再迁移，不启 backend/frontend）
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

# 日志目录与文件
LOG_DIR="$PROJECT_DIR/logs"
LOG_FILE="$LOG_DIR/deploy_$(date +%F).log"
mkdir -p "$LOG_DIR"

# ============================================================
# 工具：分级日志（带时间戳，stdout + 追加写入日志文件）
# ============================================================
_ts() { date '+%Y-%m-%d %H:%M:%S'; }
log_info()  { echo "[INFO]  $(_ts)  $*" | tee -a "$LOG_FILE"; }
log_ok()    { echo "[OK]    $(_ts)  $*" | tee -a "$LOG_FILE"; }
log_warn()  { echo "[WARN]  $(_ts)  $*" | tee -a "$LOG_FILE" >&2; }
log_error() { echo "[ERROR] $(_ts)  $*" | tee -a "$LOG_FILE" >&2; }

# 确保共享网关网络存在（网关项目创建同名网络，这里兜底）
docker network inspect edge-net >/dev/null 2>&1 || docker network create edge-net

# ============================================================
# 数据库迁移相关函数
# ============================================================

# 等待 db 容器变为 healthy（最多 120s）
_wait_db_healthy() {
  local max_wait=120
  local waited=0
  log_info "等待数据库容器变为 healthy（最长 ${max_wait}s）..."
  while (( waited < max_wait )); do
    local state
    state="$("${COMPOSE[@]}" ps --format json db 2>/dev/null \
      | python3 -c 'import sys,json; d=json.loads(sys.stdin.read() or "{}"); print(d.get("State",""))' 2>/dev/null || true)"
    if [[ "$state" == "running" ]]; then
      local health
      health="$("${COMPOSE[@]}" ps --format json db 2>/dev/null \
        | python3 -c 'import sys,json; d=json.loads(sys.stdin.read() or "{}"); print(d.get("Health",""))' 2>/dev/null || true)"
      if [[ "$health" == "healthy" ]]; then
        log_ok "数据库容器 healthy，耗时 ${waited}s"
        return 0
      fi
    fi
    sleep 5
    waited=$(( waited + 5 ))
  done
  log_error "等待数据库 healthy 超时（${max_wait}s），请检查 db 容器日志: ${COMPOSE[*]} logs db"
  return 1
}

# 环境校验：migrate 执行前检查
#   1. backend 镜像已构建（或容器可 run 起来）
#   2. db 已 healthy
#   3. manage.py 存在且可调用（--version 能跑通）
_validate_migrate_env() {
  log_info "=== 数据库迁移环境校验开始 ==="

  # 1) 确认 backend 镜像存在（避免 compose run 时才去 build 才发现失败
  local backend_img
  backend_img="$("${COMPOSE[@]}" config --format json 2>/dev/null \
    | python3 -c 'import sys,json
c=json.loads(sys.stdin.read())
svcs=c.get("services",{})
b=svcs.get("backend",{})
print(b.get("image",""))' 2>/dev/null || true)"
  if [[ -n "$backend_img" ]]; then
    if ! docker image inspect "$backend_img" >/dev/null 2>&1; then
      log_warn "backend 镜像 ($backend_img) 尚未构建，先执行 build..."
      "${COMPOSE[@]}" build backend
    fi
  fi

  # 2) 启动 db（如果没启动），并等待 healthy
  local db_state
  db_state="$("${COMPOSE[@]}" ps --status running --format json db 2>/dev/null \
    | python3 -c 'import sys,json
try:
    data=json.loads(sys.stdin.read() or "{}")
    # docker compose ps format json 在单服务时可能返回 dict 或 list
    if isinstance(data, list):
        print(any(x.get("Service")=="db" or x.get("Name","").endswith("-db") for x in data) and "running" or "")
    else:
        print(data.get("State",""))
except Exception:
    print("")' 2>/dev/null || true)"
  if [[ "$db_state" != "running" ]]; then
    log_info "数据库容器未运行，先启动 db..."
    "${COMPOSE[@]}" up -d db
  fi
  _wait_db_healthy || return 1

  # 3) 用一次性 run 调 manage.py version，确认 Django + DB 连通无误
  log_info "验证 Django manage.py 与数据库连接（调用 manage.py check --database default）..."
  if ! "${COMPOSE[@]}" run --rm --no-deps backend \
        python manage.py check --database default >>"$LOG_FILE" 2>&1; then
    log_error "Django check 失败，可能原因：
  1) 数据库账号/密码与 docker.env 不一致
  2) 数据库尚未初始化 / 库未创建
  3) 网络不通（backend 与 db 容器不在同一 docker network）
请查看日志: tail -50 $LOG_FILE"
    return 1
  fi

  log_ok "=== 数据库迁移环境校验通过 ==="
  return 0
}

# 执行数据库迁移
#  - 先 showmigrations 统计待迁移数量
#  - 0 个：跳过并打印提示
#  - >0 个：记录耗时后执行 migrate --noinput，失败立即返回非零
run_migrate() {
  log_info "=== 数据库迁移流程开始 ==="
  local start_ts end_ts elapsed

  _validate_migrate_env || { log_error "迁移前环境校验失败，终止部署"; return 1; }

  # 统计未应用迁移数（每行可能有前导空格，未应用的中括号里为空格 "[ ]"，已应用为 "[X]"）
  log_info "检查待应用的数据库迁移..."
  local pending
  pending="$("${COMPOSE[@]}" run --rm --no-deps backend \
      python manage.py showmigrations --plan 2>>"$LOG_FILE" \
    | grep -cE '^[[:space:]]*\[[[:space:]]\]' || true)"

  if [[ "${pending:-0}" -eq 0 ]]; then
    log_ok "未检测到待应用的数据库迁移（pending=0），自动跳过迁移步骤"
    log_ok "=== 数据库迁移流程结束（无需变更） ==="
    return 0
  fi

  log_info "检测到 ${pending} 个待应用迁移，以下为迁移计划："
  "${COMPOSE[@]}" run --rm --no-deps backend \
    python manage.py showmigrations --plan 2>>"$LOG_FILE" \
    | grep -E '^[[:space:]]*\[[[:space:]]\]' | tee -a "$LOG_FILE" || true

  start_ts=$(date +%s)
  log_info "开始执行 migrate --noinput ..."
  if ! "${COMPOSE[@]}" run --rm --no-deps backend \
        python manage.py migrate --noinput >>"$LOG_FILE" 2>&1; then
    end_ts=$(date +%s)
    elapsed=$(( end_ts - start_ts ))
    log_error "数据库迁移执行失败！耗时 ${elapsed}s。
  终止后续部署流程。
  详细日志请查看: tail -100 $LOG_FILE
  常见原因：
    1) 迁移文件与现有表结构冲突
    2) 数据库账号缺少 ALTER/CREATE 权限
    3) 迁移文件缺失依赖（漏提交了 00xx_*.py）
  建议：先手动进入容器定位：
    ${COMPOSE[*]} run --rm backend python manage.py migrate --noinput"
    return 1
  fi

  end_ts=$(date +%s)
  elapsed=$(( end_ts - start_ts ))
  log_ok "数据库迁移执行成功，耗时 ${elapsed}s，共应用 ${pending} 个迁移"

  # 迁移完成后再 showmigrations 全应为 [X]，输出确认
  local remaining
  remaining="$("${COMPOSE[@]}" run --rm --no-deps backend \
      python manage.py showmigrations --plan 2>>"$LOG_FILE" \
    | grep -cE '^[[:space:]]*\[[[:space:]]\]' || true)"
  if [[ "${remaining:-0}" -ne 0 ]]; then
    log_warn "迁移后仍有 ${remaining} 个未应用迁移，请人工确认（showmigrations 输出已写入日志）"
  else
    log_ok "迁移复核通过：所有迁移均已应用"
  fi

  log_ok "=== 数据库迁移流程结束 ==="
  return 0
}

# ============================================================
# 命令分发
# ============================================================
cmd="${1:-up}"

case "$cmd" in
  build)
    log_info "执行 build：构建 backend + frontend 镜像"
    "${COMPOSE[@]}" build
    log_ok "build 完成"
    ;;
  up)
    log_info "=== 部署 up 流程开始 ==="

    # 1) 先构建镜像（与原行为一致：--build）
    log_info "[1/3] 构建镜像（docker compose up --build）..."
    "${COMPOSE[@]}" build backend frontend

    # 2) 在应用服务启动前，完成数据库迁移（迁移内部会 up db + 等 healthy）
    log_info "[2/3] 执行数据库迁移（应用服务启动前）..."
    run_migrate || {
      log_error "部署中止：数据库迁移失败，未启动 backend/frontend 服务"
      exit 1
    }

    # 3) 最后启动全部服务（-d 后台）
    log_info "[3/3] 启动全部服务（db/backend/frontend）..."
    "${COMPOSE[@]}" up -d
    "${COMPOSE[@]}" ps
    log_ok "=== 部署 up 流程完成 ==="
    ;;
  migrate)
    run_migrate || exit 1
    ;;
  restart)
    log_info "=== 部署 restart 流程开始 ==="

    # restart 前也先跑一次迁移：新镜像可能带了新的 migration
    log_info "[1/2] 重启前执行数据库迁移..."
    run_migrate || {
      log_error "重启中止：数据库迁移失败"
      exit 1
    }

    log_info "[2/2] 重启全部服务..."
    "${COMPOSE[@]}" restart
    "${COMPOSE[@]}" ps
    log_ok "=== restart 流程完成 ==="
    ;;
  down)
    log_info "执行 down：停止并移除容器（保留数据卷）"
    "${COMPOSE[@]}" down
    log_ok "down 完成"
    ;;
  logs)
    "${COMPOSE[@]}" logs -f --tail=100
    ;;
  ps)
    "${COMPOSE[@]}" ps
    ;;
  init-db)
    # 导入数据快照（表已存在时先 DROP 再重建，内容以快照为准）
    log_info "执行 init-db：导入数据快照"
    set -a; source "$ENV_FILE"; set +a
    log_info "导入 doc/pangliantagege0402.sql -> ${DB_NAME:-pangliantagege}"

    # 先确保 db 已启动 healthy
    "${COMPOSE[@]}" up -d db
    _wait_db_healthy || { log_error "数据库未就绪，init-db 中止"; exit 1; }

    "${COMPOSE[@]}" exec -T db \
      mysql -uroot -p"${MYSQL_ROOT_PASSWORD:-${DB_PASSWORD:-root}}" "${DB_NAME:-pangliantagege}" \
      < doc/pangliantagege0402.sql \
      >>"$LOG_FILE" 2>&1
    log_ok "数据导入完成"

    # 导入后立即 migrate，保证快照 + 新的 migration 都应用（幂等）
    log_info "快照导入完成后执行迁移，确保 schema 最新..."
    run_migrate || { log_error "快照导入后迁移失败，请排查"; exit 1; }
    ;;
  seed)
    log_info "执行 seed：填充演示数据"
    "${COMPOSE[@]}" run --rm backend python populate_db.py >>"$LOG_FILE" 2>&1
    "${COMPOSE[@]}" run --rm backend python populate_techstack.py >>"$LOG_FILE" 2>&1
    log_ok "演示数据填充完成"
    ;;
  *)
    echo "用法: bash scripts/docker-deploy.sh [build|up|migrate|restart|down|logs|ps|init-db|seed]"
    exit 1
    ;;
esac
