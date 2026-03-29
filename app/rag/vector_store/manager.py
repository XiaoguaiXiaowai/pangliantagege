from pathlib import Path
from typing import List

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings

from app.core.config import Settings


class VectorStoreManager:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.persist_directory = Path(settings.chroma_persist_directory)
        self.persist_directory.mkdir(parents=True, exist_ok=True)
        
        self.embeddings = OllamaEmbeddings(
            model=settings.ollama_embed_model,
            base_url=settings.ollama_base_url,
        )
        
        self.vector_store = Chroma(
            collection_name=settings.chroma_collection_name,
            persist_directory=str(self.persist_directory),
            embedding_function=self.embeddings,
        )

    def add_documents(self, documents: List[Document]) -> List[str]:
        return self.vector_store.add_documents(documents)

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        return self.vector_store.similarity_search(query, k=k)

    def get_retriever(self, k: int = 4):
        return self.vector_store.as_retriever(search_kwargs={"k": k})
