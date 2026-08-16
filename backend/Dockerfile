# ============================================================
# PangLianTaGeGe 后端 (Django) 镜像
# 基于 python:3.12-slim，依赖均有 manylinux wheel，无需编译工具链
# ============================================================
FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# 先装依赖，充分利用构建缓存
COPY requirements.txt .
RUN pip install --upgrade pip wheel && \
    pip install -r requirements.txt

# 拷贝项目代码（.dockerignore 排除了 venv / db.sqlite3 / media 等）
COPY . .

EXPOSE 8000

# 启动流程：
#   1. migrate          —— 幂等，空库建表 / 已导入数据时自动跳过
#   2. collectstatic    —— 产出静态文件到 /app/staticfiles（宿主机可挂载）
#   3. gunicorn         —— WSGI 服务（服务器为 2 核，2 个 worker 足够）
CMD ["sh", "-c", "python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput && \
    exec gunicorn -w 2 -b 0.0.0.0:8000 config.wsgi:application"]
