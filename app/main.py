import logging
import sys

from fastapi import FastAPI
from prometheus_fastapi_instrumentator import Instrumentator

from app.api.routes.rag import router as rag_router
from app.api.routes.system import router as system_router
from app.core.config import get_settings


# 1. 简单的结构化日志配置
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger(__name__)

settings = get_settings()

app = FastAPI(title=settings.app_name)

# 2. 挂载路由
app.include_router(system_router)
app.include_router(rag_router)

# 3. 挂载 Prometheus 指标采集
instrumentator = Instrumentator(
    should_group_status_codes=False,
    should_ignore_untemplated=True,
    should_instrument_requests_inprogress=True,
    excluded_handlers=[".*admin.*", "/metrics"],
    env_var_name="ENABLE_METRICS",
    inprogress_name="inprogress",
    inprogress_labels=True,
)
instrumentator.instrument(app).expose(app)

@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.app_name} in {settings.app_env} environment...")


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": f"{settings.app_name} is running"}
