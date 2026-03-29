FROM python:3.12-slim as builder

# 设置环境变量，防止 python 写 .pyc 文件，并设置 pip 行为
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /build

# 安装构建依赖（如果有需要编译 C 扩展的包，比如 chroma 或 pymupdf，可能需要）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 先复制 pyproject.toml，利用 Docker 缓存加速依赖安装
COPY pyproject.toml .
# 创建一个假的 app 目录骗过 pip install -e 的包发现
RUN mkdir app && touch app/__init__.py

# 安装主依赖到 /opt/venv
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
# 这里我们用普通安装而不是 editable 安装
RUN pip install .

# ==========================================
# 运行阶段
# ==========================================
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    APP_ENV=production

WORKDIR /app

# 安装运行时可能需要的系统依赖 (如果有)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 从构建阶段拷贝编译好的虚拟环境
COPY --from=builder /opt/venv /opt/venv

# 拷贝项目代码
COPY app/ ./app/
COPY data/ ./data/
# 保证 data 目录有写入权限（给 chroma 和 上传文件用）
RUN chmod -R 777 ./data

# 暴露端口
EXPOSE 8000

# 启动服务
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
