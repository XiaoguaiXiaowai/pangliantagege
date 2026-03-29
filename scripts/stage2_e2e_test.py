import asyncio
import json
from pathlib import Path

import httpx

from app.core.config import get_settings


async def main():
    settings = get_settings()
    base_url = f"http://{settings.app_host}:{settings.app_port}/api"
    
    print("🚀 开始阶段二端到端测试 (请确保 FastAPI 服务已启动)...\n")
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        # 1. 测试网页导入
        print("1️⃣ 测试导入网页知识...")
        test_url = "https://python.langchain.com/v0.2/docs/introduction/"
        try:
            response = await client.post(
                f"{base_url}/documents/upload/url",
                json={"url": test_url}
            )
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2, ensure_ascii=False)}\n")
        except Exception as e:
            print(f"❌ 网页导入失败: {e}\n")

        # 2. 测试问答
        print("2️⃣ 测试 RAG 问答...")
        question = "What is LangChain?"
        print(f"Question: {question}")
        try:
            response = await client.post(
                f"{base_url}/chat",
                json={"question": question}
            )
            print(f"Status: {response.status_code}")
            result = response.json()
            print(f"Answer: {result.get('answer', '')}")
            print(f"Sources retrieved: {len(result.get('source_documents', []))}\n")
        except Exception as e:
            print(f"❌ 问答请求失败: {e}\n")

if __name__ == "__main__":
    asyncio.run(main())
