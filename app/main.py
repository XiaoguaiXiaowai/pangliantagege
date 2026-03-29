from fastapi import FastAPI

from app.api.routes.rag import router as rag_router
from app.api.routes.system import router as system_router
from app.core.config import get_settings
from app.core.runtime import ensure_supported_python


ensure_supported_python()
settings = get_settings()

app = FastAPI(title=settings.app_name)
app.include_router(system_router)
app.include_router(rag_router)


@app.get("/")
async def root() -> dict[str, str]:
    return {"message": f"{settings.app_name} is running"}
