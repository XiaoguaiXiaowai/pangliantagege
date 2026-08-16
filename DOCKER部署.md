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
