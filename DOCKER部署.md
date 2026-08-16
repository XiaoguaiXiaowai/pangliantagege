# PangLianTaGeGe Docker 部署说明

本文档介绍如何用 Docker Compose 部署本项目，并重点说明**如何让另一个容器项目与本项目共用同一套域名和 HTTPS 证书**。

---

## 1. 架构总览

```
                         ┌────────────────────────────────────┐
                         │  gateway/ 共享网关 (nginx:1.27)     │
   Internet ── 80/443 ──▶│  独占 80/443，挂载 https/ 证书      │
   (TLS 在此终结)         │  按 server_name 路由到各项目        │
                         └──────────────┬─────────────────────┘
                                        │ docker network: edge-net（共享）
              ┌─────────────────────────┴─────────────────────────┐
              │                                                   │
   ┌──────────▼───────────┐                          ┌────────────▼───────────┐
   │ pltgg 项目 (本项目)    │                          │ 另一个容器项目          │
   │                      │                          │ (例: myapp:3000)       │
   │ pltgg-frontend :80   │                          │ 加入 edge-net 网络      │
   │  (nginx: 静态页+反代) │                          │ 在网关配置中加 server 块 │
   │   └▶ pltgg-backend   │                          └────────────────────────┘
   │        └▶ pltgg-db   │
   └──────────────────────┘
```

关键设计：

| 组件 | 说明 |
|---|---|
| `gateway/` | 共享网关 nginx 容器，**唯一**绑定宿主机 80/443，挂载 `https/` 证书目录（只读）。两个项目都通过它接入 |
| `edge-net` | 共享 Docker 网络，网关和各项目容器都在此网络内，用容器名互相访问 |
| `pltgg-frontend` | 本项目前端 nginx：托管 Vue 构建产物，直接服务 `/media/` `/static/`，反代 `/api/` `/admin/` 到后端 |
| `pltgg-backend` | Django + gunicorn，启动时自动 `migrate` + `collectstatic` |
| `pltgg-db` | MySQL 8.0 容器，数据在 `mysql_data` 卷中 |

> **为什么需要网关？** 80/443 端口同一台机器只能被一个进程占用。两个项目各自起 nginx 会冲突；证书也只挂载一份、只在一个地方续期。网关把"入口/证书"与"应用"解耦，任何项目升级、重启都不影响入口。

---

## 2. 快速开始（仅本项目）

### 2.1 准备

```bash
# 1) 配置环境变量（改密码！）
cp docker.env.example docker.env
vim docker.env

# 2) 确保共享网络存在（网关项目创建同名网络，这里兜底）
docker network create edge-net || true
```

### 2.2 启动

```bash
# 构建并后台启动（db + backend + frontend）
docker compose --env-file docker.env up -d --build

# 查看状态（等待 db healthy、backend 完成迁移）
docker compose --env-file docker.env ps
```

### 2.3 初始化数据（二选一）

**方式 A：导入现成数据快照（推荐，含简历/音乐/管理员等真实数据）**

```bash
bash scripts/docker-deploy.sh init-db
```

**方式 B：空库 + 示例数据**

```bash
bash scripts/docker-deploy.sh seed
```

### 2.4 启动共享网关（对外提供服务）

```bash
cd gateway
docker compose up -d        # 默认 80/443
cd ..
```

然后访问 `https://www.pangliantagege.top`。

> 本地联调不想占 80/443 时：`cd gateway && HTTP_PORT=8080 HTTPS_PORT=8443 docker compose up -d`，再用
> `curl --resolve www.pangliantagege.top:8443:127.0.0.1 -k https://www.pangliantagege.top/` 验证。

### 2.5 日常运维

```bash
bash scripts/docker-deploy.sh ps        # 状态
bash scripts/docker-deploy.sh logs      # 日志
bash scripts/docker-deploy.sh restart   # 重启
bash scripts/docker-deploy.sh down      # 停止（数据卷保留）

# 更新代码后重新部署
git pull
docker compose --env-file docker.env up -d --build
```

---

## 3. 让另一个容器项目共用这套域名和 HTTPS 证书

这是最常见的问题。核心思想：**入口只有一个（网关），项目各自躲在内部网络里，网关按域名转发。**

### 3.1 新项目侧（以 compose 项目 myapp 为例）

在其 `docker-compose.yml` 中加入共享网络：

```yaml
name: myapp

services:
  web:
    build: .
    container_name: myapp-web        # 网关用这个容器名转发
    # 不需要 ports: 对外映射！由网关统一入口
    networks:
      - myapp-net                    # 自己的内部网络（可选）
      - edge-net                     # 共享网络，必须

networks:
  myapp-net:
  edge-net:
    external: true                   # 已由网关项目创建
```

### 3.2 证书侧

把该项目的证书文件放入本仓库根目录 `https/`（网关已把 `../https` 挂载为容器内 `/etc/nginx/https`），例如：

```text
https/
├── www.pangliantagege.top.pem/.key     # 本站
└── myapp.example.com.pem/.key          # 新项目
```

> 若使用 Let's Encrypt 等自动续期，只需保证续期脚本写回 `https/` 目录，然后
> `docker compose -f gateway/docker-compose.yml exec gateway nginx -s reload` 即可生效，无需重建任何项目容器。

### 3.3 网关侧

编辑 `gateway/nginx.conf`，按文末模板添加 server 块：

```nginx
server {
    listen 80;
    server_name myapp.example.com;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl;
    http2 on;
    server_name myapp.example.com;

    ssl_certificate     /etc/nginx/https/myapp.example.com.pem;
    ssl_certificate_key /etc/nginx/https/myapp.example.com.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    client_max_body_size 20M;

    location / {
        set $myapp_upstream http://myapp-web;   # 容器名（需在 edge-net 网络内）
        proxy_pass $myapp_upstream;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3.4 生效

```bash
cd gateway
docker compose up -d --force-recreate   # 或仅重载配置：
docker compose exec gateway nginx -s reload
```

DNS 把 `myapp.example.com` 解析到本机后即可访问。

> **也可以按路径分流**（如 `pangliantagege.top/app2/` 转发到另一项目），把网关里的 `server_name` 换成 `location /app2/` 并在 `proxy_pass` 前做路径重写即可，原理相同。

---

## 4. 数据与备份

| 数据 | 位置 | 说明 |
|---|---|---|
| MySQL 数据 | docker 卷 `mysql_data` | `docker volume ls` 查看 |
| 上传媒体 | `./backend/media/` | 宿主机目录，直接打包备份 |
| 静态文件 | `./backend/staticfiles/` | 可随时由 collectstatic 重建，无需备份 |

备份数据库：

```bash
docker compose --env-file docker.env exec db \
  mysqldump -uroot -p"$MYSQL_ROOT_PASSWORD" pangliantagege > backup_$(date +%F).sql
```

---

## 5. 常见问题

**Q: 后端启动失败，日志提示数据库连不上？**
A: 等待 MySQL 首次初始化（约 20-60s），`docker compose ps` 中 db 变为 healthy 后 backend 会自动启动。若反复失败检查 `docker.env` 中密码是否与 `MYSQL_ROOT_PASSWORD` 一致（backend 用 `DB_PASSWORD`）。

**Q: 导入数据快照报错？**
A: 快照 `doc/pangliantagege0402.sql` 含 `DROP TABLE IF EXISTS`，会覆盖当前数据，仅在首次部署或确定要回滚数据时执行。

**Q: 证书更新后不生效？**
A: 证书是挂载进网关容器的（只读），替换文件后 `docker compose -f gateway/docker-compose.yml exec gateway nginx -s reload`；若证书文件名变了需要同步修改 `gateway/nginx.conf` 并 `docker compose -f gateway/docker-compose.yml up -d`。

**Q: 前端页面能打开但 API 404？**
A: 检查 `docker.env` 中 `ALLOWED_HOSTS` 是否包含访问域名；检查 gateway 是否把请求转发到了 `pltgg-frontend`（`docker compose -f gateway/docker-compose.yml logs gateway`）。

**Q: AI 聊天（/api/chat）如何恢复？**
A: 当前按需求暂不代理。恢复步骤：① `docker.env` 设置 `RAG_PROXY_TARGET=host:port`；② 取消 `frontend/nginx.conf` 中 `/api/chat` 注释；③ 重新构建前端 `docker compose --env-file docker.env up -d --build frontend`。

**Q: 与旧的 deploy.sh / systemd 部署冲突吗？**
A: 不冲突，旧方案保留未动。注意二者不能同时运行（都会占用 80/443、8000 端口），切换前先停掉旧服务。

---

## 6. 服务器实测部署记录（8.140.233.55，2026-08-16）

> 本仓库已在生产服务器完成 Docker 化部署并验证通过。以下为实测拓扑与关键步骤，新服务器可照此复现。

### 6.1 实际拓扑（宿主机 nginx 作共享网关）

```
Internet → 宿主机 nginx (80/443, TLS)      ← 唯一入口（nginx 1.24 + 手动证书）
             ├─ www.pangliantagege.top → 127.0.0.1:8080 → pltgg-frontend 容器
             │      (nginx: 静态页 + /media /static + 反代 /api /admin)
             │              └→ pltgg-backend 容器 (gunicorn)
             │                      └→ pltgg-db 容器 (MySQL 8, 内存瘦身)
             └─ playground.pangliantagege.top → aiepg 容器 (3000/8001, 独立项目)
```

服务器 nginx 配置：`deploy/pangliantagege.docker.conf`（本仓库已归档），
替换了原 `pangliantagege.prod.conf`（systemd 部署版）。`/api/chat`（RAG）按需求未代理。

### 6.2 部署步骤（复现）

```bash
# 1. 代码同步
git push prod master                       # 本地 → 服务器 bare repo
ssh root@8.140.233.55 'cd /opt/git/pltgg && git pull'

# 2. 环境变量（服务器上生成强密码）
ssh root@8.140.233.55 'cd /opt/git/pltgg && vim docker.env'

# 3. 镜像：本地为 ARM 架构！必须构建 amd64 版再传输
docker buildx build --platform linux/amd64 -t pltgg-backend:latest ./backend
docker buildx build --platform linux/amd64 -t pltgg-frontend:latest ./frontend
docker save pltgg-backend:latest pltgg-frontend:latest | gzip \
  | ssh root@8.140.233.55 'gunzip | docker load'

# 4. 网络与容器
ssh root@8.140.233.55 'docker network create edge-net  # 首次
cd /opt/git/pltgg && docker compose --env-file docker.env up -d db
# 等待 healthy 后导入数据（宿主机 MySQL → 容器 MySQL）
mysqldump -uroot -pXXX --single-transaction --set-gtid-purged=OFF pangliantagege \
  | docker compose --env-file docker.env exec -T db mysql -uroot -pYYY pangliantagege
docker compose --env-file docker.env up -d'

# 5. nginx 切换 + 停旧服务
ssh root@8.140.233.55 'ln -sf /etc/nginx/sites-available/pangliantagege.docker.conf /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/pangliantagege.prod.conf /etc/nginx/sites-enabled/pangliantagege.conf
nginx -t && systemctl reload nginx
systemctl disable --now plapi plui'          # 旧 systemd 服务
```

### 6.3 踩坑记录（重要）

| 问题 | 原因 | 解决 |
|---|---|---|
| 部署后服务器卡死、SSH 无响应、主站超时 | 1.6G 内存上 MySQL 容器初始化 + 旧栈满载 → swap 风暴，反复 OOM | 阿里云 API 强制重启；停旧 plapi/plui 释放 230MB；MySQL 瘦身（见下）；**先停旧服务再起新容器** |
| MySQL 容器 unhealthy / 数据文件损坏 | 首次初始化被风暴/重启中断 | `docker compose down -v` 清卷重建（无数据损失，卷内本无数据） |
| `exec format error` 容器起不来 | Mac(ARM) 构建的镜像传到 x86_64 服务器 | `buildx build --platform linux/amd64` 重新构建传输 |
| MySQL 内存占用过大 | performance_schema 默认开启 | compose 加 `--performance-schema=OFF --innodb-buffer-pool-size=64M`（~500MB→~250MB） |
| playground 502 | 强制重启后 aiepg 容器未自启（restart 策略默认 no）；且其 compose 与运行中容器不一致（端口 8001→8000） | `docker start` 旧容器 + `docker-compose.override.yml` 恢复 8001 映射（未改 aiepg 源码） |
| `edge-net` external 网络缺失 | 服务器首次部署 | `docker network create edge-net` |

### 6.4 运维备忘

- **主站证书手动维护**（用户选择）：`/var/pltgg/https/*.pem`，2026-09-06 到期，到期前需手动替换并 `systemctl reload nginx`。
- **主域名 apex（pangliantagege.top）无 DNS A 记录**：不影响 www 访问，但 apex 的 https 跳转暂不可达；需要时去阿里云 DNS 添加。
- **宿主机 MySQL 仍运行**（数据已迁移到容器，保留作备份/回滚用；book_demo 项目可能依赖，勿直接停）。
- **内存基线**：1.6G 物理 + 4G swap，7 个容器满载 ~1.3G，运行稳定；扩容前勿再加重量级容器。
- **回滚**：旧代码在 `/var/pltgg`（systemd 部署完整保留），`systemctl enable --now plapi plui` + 恢复旧 nginx 配置即可切回。

---

## 7. GitHub Actions 自动部署

代码 push 到 GitHub master 后，自动构建镜像并部署到生产服务器；也可在 GitHub Actions 页面手动触发。

### 7.1 流水线结构

```
push master (或手动触发)
   └─ job build  (ubuntu runner, amd64)
        ├─ 构建 backend 镜像 → ghcr.io/<user>/pangliantagege/pltgg-backend:latest
        └─ 构建 frontend 镜像 → ghcr.io/<user>/pangliantagege/pltgg-frontend:latest
   └─ job deploy (needs build)
        ├─ 受限 SSH → 服务器执行 scripts/remote-deploy.sh
        │     [1] git fetch GitHub master + reset --hard（代码同步，public 仓库免密）
        │     [2] docker compose pull backend frontend（ghcr 公开镜像）
        │     [3] up -d --force-recreate（容器内自动 migrate + collectstatic）
        │     [4] docker image prune 清理旧镜像
        └─ 健康检查：线上 /api/resume/ 返回 200 才算成功
```

### 7.2 涉及文件

| 文件 | 作用 |
|---|---|
| `.github/workflows/deploy.yml` | Actions 流水线（构建推 ghcr + SSH 部署 + 健康检查） |
| `scripts/remote-deploy.sh` | 服务器端部署脚本（部署位置 `/opt/git/pltgg/scripts/`） |
| `scripts/ssh-gate.sh` | 部署密钥 SSH 门卫：只放行 git 操作与部署脚本，**无法开 shell** |
| `docker-compose.yml` | 镜像名 `${IMAGE_REPO:-pltgg}/...`，生产由 docker.env 的 `IMAGE_REPO` 指向 ghcr |

### 7.3 一次性配置（服务器已就绪，以下为 GitHub 侧）

1. **仓库 Secrets**（Settings → Secrets and variables → Actions → New repository secret）：
   - `PROD_HOST` = `8.140.233.55`
   - `PROD_SSH_KEY` = 部署专用私钥（ed25519，公钥已安装到服务器且受 ssh-gate 限制）
2. **首次运行后把 ghcr 包设为 public**（否则服务器 pull 会被 denied）：
   GitHub 仓库页面 → Packages → 点开 `pangliantagege/pltgg-backend` 和 `pltgg-frontend` →
   Package settings → Danger Zone → Change visibility → Public
3. 手动触发一次：Actions 页面 → Deploy to Production → Run workflow

### 7.4 日常使用

```bash
# 部署新版本 = 正常提交并推送
git add . && git commit -m "..." && git push github master
# 回滚 = revert 后 push
git revert HEAD && git push github master
```

> 服务器上不要手动改 `/opt/git/pltgg` 下的文件（`git reset --hard` 会覆盖）；
> `docker.env` 与 `backend/media` 已 gitignore，不受影响。
> 本地测试不受影响：本地 `docker.env` 不设 `IMAGE_REPO`，compose 仍用本地构建的镜像。
