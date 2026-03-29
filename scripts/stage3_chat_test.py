import asyncio
import json

import httpx

from app.core.config import get_settings


async def main():
    settings = get_settings()
    base_url = f"http://{settings.app_host}:{settings.app_port}/api"
    
    print("🚀 开始阶段三：多轮对话能力测试...\n")
    
    async with httpx.AsyncClient(timeout=120.0) as client:
        chat_history = []
        
        # ------------------
        # 第一轮对话：提出基础问题
        # ------------------
        question_1 = "什么是 LangChain？"
        print(f"User: {question_1}")
        
        payload_1 = {
            "question": question_1,
            "chat_history": chat_history
        }
        
        try:
            response_1 = await client.post(f"{base_url}/chat", json=payload_1)
            result_1 = response_1.json()
            answer_1 = result_1.get('answer', '')
            print(f"Assistant: {answer_1}\n")
            
            # 保存到历史记录中
            chat_history.append({"role": "user", "content": question_1})
            chat_history.append({"role": "assistant", "content": answer_1})
            
        except Exception as e:
            print(f"❌ 第一轮请求失败: {e}\n")
            return

        # ------------------
        # 第二轮对话：基于上下文代词的提问 (测试它能否理解 "它")
        # ------------------
        question_2 = "它的主要组件有哪些？"
        print(f"User: {question_2}")
        
        payload_2 = {
            "question": question_2,
            "chat_history": chat_history
        }
        
        try:
            response_2 = await client.post(f"{base_url}/chat", json=payload_2)
            result_2 = response_2.json()
            answer_2 = result_2.get('answer', '')
            print(f"Assistant: {answer_2}\n")
            
            # 打印被重写后的独立问题（这步需要在服务端查看日志，但在客户端我们可以通过回答质量来推断）
            print(f"✅ 如果回答中提到了 LangChain 的组件，说明多轮对话记忆生效了。")
            
        except Exception as e:
            print(f"❌ 第二轮请求失败: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())
