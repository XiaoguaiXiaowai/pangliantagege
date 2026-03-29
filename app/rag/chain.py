from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama

from app.core.config import Settings
from app.rag.vector_store.manager import VectorStoreManager


class RAGChain:
    def __init__(self, settings: Settings, vector_store: VectorStoreManager):
        self.settings = settings
        self.vector_store = vector_store
        
        self.llm = ChatOllama(
            base_url=settings.ollama_base_url,
            model=settings.ollama_chat_model,
            temperature=0,
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个专业的知识库问答助手。请仅根据下面提供的上下文信息回答问题。如果上下文中没有相关信息，请回答“我不知道”，不要编造答案。"),
            ("human", "上下文信息：\n{context}\n\n问题：{question}")
        ])

    @staticmethod
    def format_docs(docs: list[Document]) -> str:
        return "\n\n".join(doc.page_content for doc in docs)

    async def ainvoke(self, question: str) -> dict[str, object]:
        retriever = self.vector_store.get_retriever()
        
        rag_chain_from_docs = (
            RunnablePassthrough.assign(context=(lambda x: self.format_docs(x["context"])))
            | self.prompt
            | self.llm
            | StrOutputParser()
        )
        
        rag_chain_with_source = RunnablePassthrough.assign(
            context=lambda x: retriever.invoke(x["question"])
        ).assign(answer=rag_chain_from_docs)

        result = rag_chain_with_source.invoke({"question": question})
        
        return {
            "answer": result["answer"],
            "source_documents": [doc.page_content for doc in result["context"]]
        }
