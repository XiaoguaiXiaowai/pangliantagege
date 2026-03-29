import asyncio
import json

from app.core.config import get_settings
from app.core.runtime import ensure_supported_python
from app.services.ollama_client import OllamaClient


async def main() -> None:
    ensure_supported_python()

    from app.rag.preflight import run_preflight

    settings = get_settings()
    ollama_client = OllamaClient(settings)
    available_models = await ollama_client.list_models()
    reachable = await ollama_client.is_reachable()

    payload: dict[str, object] = {
        "ollama_base_url": settings.ollama_base_url,
        "chat_model": settings.ollama_chat_model,
        "embed_model": settings.ollama_embed_model,
        "chroma_collection": settings.chroma_collection_name,
        "ollama_reachable": reachable,
        "available_models": available_models,
    }

    if reachable:
        try:
            payload["preflight"] = await run_preflight(settings)
        except Exception as exc:
            payload["preflight_error"] = str(exc)

    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    asyncio.run(main())
