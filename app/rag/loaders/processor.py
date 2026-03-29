from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyMuPDFLoader, WebBaseLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import Settings


class DocumentProcessor:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )

    def load_pdf(self, file_path: str | Path) -> List[Document]:
        loader = PyMuPDFLoader(str(file_path))
        return loader.load()

    def load_web(self, url: str) -> List[Document]:
        loader = WebBaseLoader(url)
        return loader.load()

    def split_documents(self, documents: List[Document]) -> List[Document]:
        return self.text_splitter.split_documents(documents)

    def process_file(self, file_path: str | Path) -> List[Document]:
        docs = self.load_pdf(file_path)
        return self.split_documents(docs)

    def process_url(self, url: str) -> List[Document]:
        docs = self.load_web(url)
        return self.split_documents(docs)
