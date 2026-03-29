from __future__ import annotations

from typing import Any

import httpx

from app.core.config import Settings


class OllamaClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    async def _get_tags_payload(self) -> dict[str, Any] | None:
        try:
            async with httpx.AsyncClient(base_url=self._settings.ollama_base_url, timeout=5.0) as client:
                response = await client.get("/api/tags")
                response.raise_for_status()
        except httpx.HTTPError:
            return None

        payload: dict[str, Any] = response.json()
        return payload

    async def list_models(self) -> list[str]:
        payload = await self._get_tags_payload()
        if payload is None:
            return []

        models = payload.get("models", [])
        return [model.get("name", "") for model in models if model.get("name")]

    async def is_reachable(self) -> bool:
        payload = await self._get_tags_payload()
        return payload is not None
