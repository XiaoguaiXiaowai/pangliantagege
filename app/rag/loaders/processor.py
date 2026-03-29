from pathlib import Path
from typing import List

from langchain_community.document_loaders import PyMuPDFLoader, WebBaseLoader, UnstructuredMarkdownLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.core.config import Settings


class DocumentProcessor:
    def __init__(self, settings: Settings):
        self.settings = settings
        # 使用 RecursiveCharacterTextSplitter，它会优先按段落、句子切分，比单纯按字符切分更合理
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            separators=["\n\n", "\n", "。", "！", "？", " ", ""],
        )

    def load_pdf(self, file_path: str | Path) -> List[Document]:
        loader = PyMuPDFLoader(str(file_path))
        return loader.load()
        
    def load_markdown(self, file_path: str | Path) -> List[Document]:
        loader = UnstructuredMarkdownLoader(str(file_path))
        return loader.load()

    def load_web(self, url: str) -> List[Document]:
        loader = WebBaseLoader(url)
        return loader.load()

    def split_documents(self, documents: List[Document]) -> List[Document]:
        return self.text_splitter.split_documents(documents)

    def process_file(self, file_path: str | Path) -> List[Document]:
        file_path_str = str(file_path).lower()
        if file_path_str.endswith(".pdf"):
            docs = self.load_pdf(file_path)
        elif file_path_str.endswith(".md"):
            docs = self.load_markdown(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path}")
            
        return self.split_documents(docs)

    def process_url(self, url: str) -> List[Document]:
        docs = self.load_web(url)
        return self.split_documents(docs)
