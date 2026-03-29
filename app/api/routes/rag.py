import shutil
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from app.core.config import Settings, get_settings
from app.rag.chain import RAGChain
from app.rag.loaders.processor import DocumentProcessor
from app.rag.vector_store.manager import VectorStoreManager
from app.schemas.rag import ChatRequest, ChatResponse, UploadResponse, UrlUploadRequest


router = APIRouter(prefix="/api", tags=["rag"])


def get_document_processor(settings: Settings = Depends(get_settings)) -> DocumentProcessor:
    return DocumentProcessor(settings)


def get_vector_store(settings: Settings = Depends(get_settings)) -> VectorStoreManager:
    return VectorStoreManager(settings)


def get_rag_chain(
    settings: Settings = Depends(get_settings),
    vector_store: VectorStoreManager = Depends(get_vector_store),
) -> RAGChain:
    return RAGChain(settings, vector_store)


@router.post("/documents/upload/file", response_model=UploadResponse)
async def upload_document(
    file: UploadFile = File(...),
    settings: Settings = Depends(get_settings),
    processor: DocumentProcessor = Depends(get_document_processor),
    vector_store: VectorStoreManager = Depends(get_vector_store),
) -> UploadResponse:
    if not file.filename or not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    upload_dir = Path(settings.upload_directory)
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    file_path = upload_dir / file.filename
    try:
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        docs = processor.process_file(file_path)
        if not docs:
            raise HTTPException(status_code=400, detail="No content could be extracted from the file")
            
        vector_store.add_documents(docs)
        
        return UploadResponse(
            message=f"Successfully processed {file.filename}",
            num_chunks=len(docs),
        )
    finally:
        # 即使入库失败，也最好清理一下临时文件，或者你也可以选择保留作备查
        pass


@router.post("/documents/upload/url", response_model=UploadResponse)
async def upload_url(
    request: UrlUploadRequest,
    processor: DocumentProcessor = Depends(get_document_processor),
    vector_store: VectorStoreManager = Depends(get_vector_store),
) -> UploadResponse:
    try:
        docs = processor.process_url(request.url)
        if not docs:
            raise HTTPException(status_code=400, detail="No content could be extracted from the URL")
            
        vector_store.add_documents(docs)
        
        return UploadResponse(
            message=f"Successfully processed URL",
            num_chunks=len(docs),
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/chat", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    rag_chain: RAGChain = Depends(get_rag_chain),
) -> dict[str, object]:
    try:
        result = await rag_chain.ainvoke(
            question=request.question,
            chat_history=request.chat_history
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
