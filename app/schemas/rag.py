from typing import List, Dict, Optional

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., description="用户提问")
    chat_history: Optional[List[Dict[str, str]]] = Field(
        default=None, 
        description="对话历史，格式如 [{'role': 'user', 'content': 'hi'}, {'role': 'assistant', 'content': 'hello'}]"
    )


class ChatResponse(BaseModel):
    answer: str = Field(..., description="LLM 回答")
    source_documents: list[str] = Field(..., description="参考的文档片段")


class UrlUploadRequest(BaseModel):
    url: str = Field(..., description="网页 URL")


class UploadResponse(BaseModel):
    message: str = Field(..., description="处理结果信息")
    num_chunks: int = Field(..., description="切分后的片段数量")
