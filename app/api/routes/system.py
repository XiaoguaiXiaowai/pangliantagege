from fastapi import APIRouter, Depends

from app.core.config import Settings, get_settings
from app.schemas.system import HealthResponse
from app.services.ollama_client import OllamaClient


router = APIRouter(prefix="/system", tags=["system"])


@router.get("/health", response_model=HealthResponse)
async def health(settings: Settings = Depends(get_settings)) -> HealthResponse:
    return HealthResponse(
        status="ok",
        app_name=settings.app_name,
        environment=settings.app_env,
    )


@router.get("/probe")
async def probe(settings: Settings = Depends(get_settings)) -> dict[str, object]:
    ollama_client = OllamaClient(settings)
    available_models = await ollama_client.list_models()
    ollama_reachable = await ollama_client.is_reachable()

    response: dict[str, object] = {
        "status": "ok" if ollama_reachable else "degraded",
        "base_url": settings.ollama_base_url,
        "chat_model": settings.ollama_chat_model,
        "embed_model": settings.ollama_embed_model,
        "chroma_collection": settings.chroma_collection_name,
        "ollama_reachable": ollama_reachable,
        "available_models": available_models,
    }

    if ollama_reachable:
        try:
            from app.rag.preflight import run_preflight

            response["preflight"] = await run_preflight(settings)
        except Exception as exc:
            response["status"] = "degraded"
            response["preflight_error"] = str(exc)

    return response
