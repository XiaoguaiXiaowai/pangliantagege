from app.core.config import Settings
from app.core.runtime import ensure_supported_python


async def run_preflight(settings: Settings) -> dict[str, object]:
    ensure_supported_python()

    from langchain_chroma import Chroma
    from langchain_core.documents import Document
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_ollama import ChatOllama, OllamaEmbeddings

    embeddings = OllamaEmbeddings(
        model=settings.ollama_embed_model,
        base_url=settings.ollama_base_url,
    )

    vector_store = Chroma(
        collection_name=f"{settings.chroma_collection_name}-preflight",
        embedding_function=embeddings,
    )

    documents = [
        Document(page_content="RAG 是检索增强生成的简称。"),
        Document(page_content="FastAPI 常用于构建高性能 Python API 服务。"),
        Document(page_content="Chroma 可以作为本地向量数据库使用。"),
    ]

    vector_store.add_documents(documents)
    retrieved_docs = vector_store.similarity_search("什么适合做本地向量数据库？", k=2)

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "你是一个简洁的技术助手。"),
            ("human", "仅根据以下上下文回答问题。\n上下文：{context}\n问题：{question}"),
        ]
    )
    llm = ChatOllama(
        base_url=settings.ollama_base_url,
        model=settings.ollama_chat_model,
        temperature=0,
    )
    chain = prompt | llm
    response = await chain.ainvoke(
        {
            "context": "\n".join(doc.page_content for doc in retrieved_docs),
            "question": "本地向量数据库可以用什么？",
        }
    )

    return {
        "retrieved_docs": [doc.page_content for doc in retrieved_docs],
        "llm_response": response.content,
    }
