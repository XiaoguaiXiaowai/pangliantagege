from locust import HttpUser, task, between


class RagApiUser(HttpUser):
    # 模拟用户思考时间，每次任务间隔 1 到 3 秒
    wait_time = between(1, 3)

    @task(3)
    def check_health(self):
        """
        测试轻量级健康检查接口，权重较高 (3)，代表这是高频操作。
        主要用于评估基础 Web 框架的吞吐量上限。
        """
        self.client.get("/system/health", name="GET /system/health")

    @task(1)
    def test_chat(self):
        """
        测试核心的 RAG 对话接口，权重较低 (1)，因为大模型推理很耗时。
        这里的耗时主要取决于 Ollama 的生成速度。
        """
        payload = {
            "question": "简单介绍一下 RAG",
            "chat_history": []
        }
        self.client.post("/api/chat", json=payload, name="POST /api/chat")
