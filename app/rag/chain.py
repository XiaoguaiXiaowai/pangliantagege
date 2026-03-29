from operator import itemgetter
from typing import Dict, List, Any

from langchain_core.documents import Document
from langchain_core.messages import AIMessage, HumanMessage, get_buffer_string
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
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
        
        # 1. 独立提问的 Prompt：结合历史记录重写问题
        self.condense_question_prompt = ChatPromptTemplate.from_messages([
            ("system", "根据以下对话历史和后续的输入，重新表述后续的输入，使其成为一个独立的问题。如果没有对话历史，请原样输出后续的输入。不要回答问题，只重写它。"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}")
        ])

        # 2. 问答的 Prompt：结合检索到的上下文回答问题
        self.qa_prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一个专业的知识库问答助手。请仅根据下面提供的上下文信息回答问题。如果上下文中没有相关信息，请回答“我不知道”，不要编造答案。\n\n上下文信息：\n{context}"),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{question}")
        ])

    @staticmethod
    def format_docs(docs: list[Document]) -> str:
        return "\n\n".join(doc.page_content for doc in docs)

    def _format_chat_history(self, chat_history: List[Dict[str, str]]) -> List[Any]:
        buffer = []
        for msg in chat_history:
            role = msg.get("role", "")
            content = msg.get("content", "")
            if role == "user":
                buffer.append(HumanMessage(content=content))
            elif role == "assistant":
                buffer.append(AIMessage(content=content))
        return buffer

    async def ainvoke(self, question: str, chat_history: List[Dict[str, str]] = None) -> dict[str, object]:
        if chat_history is None:
            chat_history = []
            
        history_messages = self._format_chat_history(chat_history)
        retriever = self.vector_store.get_retriever()
        
        # 定义获取独立问题的逻辑
        condense_question_chain = (
            self.condense_question_prompt | self.llm | StrOutputParser()
        )
        
        def get_question(input_dict):
            if not input_dict.get("chat_history"):
                return input_dict["question"]
            return condense_question_chain.invoke(input_dict)
            
        # 组装完整的带有历史记录的 RAG 链
        rag_chain = (
            RunnablePassthrough.assign(
                standalone_question=RunnableLambda(get_question)
            )
            .assign(
                context=lambda x: retriever.invoke(x["standalone_question"])
            )
            .assign(
                answer=(
                    RunnablePassthrough.assign(
                        context=lambda x: self.format_docs(x["context"])
                    )
                    | self.qa_prompt
                    | self.llm
                    | StrOutputParser()
                )
            )
        )

        # 执行链
        result = rag_chain.invoke({
            "question": question,
            "chat_history": history_messages
        })
        
        return {
            "answer": result["answer"],
            "source_documents": [doc.page_content for doc in result["context"]]
        }
