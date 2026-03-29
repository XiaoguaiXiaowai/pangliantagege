from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    app_name: str
    environment: str


class ProbeResponse(BaseModel):
    status: str
    base_url: str
    chat_model: str
    embed_model: str
    chroma_collection: str
    ollama_reachable: bool
    available_models: list[str]
