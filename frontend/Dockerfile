# ============================================================
# PangLianTaGeGe 前端镜像
# 阶段一：node 构建 Vue3 静态产物（rolldown-vite）
# 阶段二：nginx 托管静态文件 + 反代 API 到后端容器
# ============================================================
FROM node:22-slim AS build

WORKDIR /app

# 先装依赖，充分利用构建缓存（rolldown-vite 使用 glibc 预编译二进制，需 debian 系基础镜像）
# NPM 镜像源：默认使用 npmmirror（原淘宝），可 --build-arg NPM_REGISTRY=https://registry.npmjs.org/ 切回官方
ARG NPM_REGISTRY=https://registry.npmmirror.com
COPY package.json package-lock.json ./
RUN npm config set registry "$NPM_REGISTRY" && \
    npm install --legacy-peer-deps

# 拷贝源码并构建
COPY . .
RUN npm run build

# ---------- 运行阶段 ----------
FROM nginx:1.27-alpine

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80
