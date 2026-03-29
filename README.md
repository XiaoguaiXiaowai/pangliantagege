# 基于 RAG 的本地化 AI 助手 (Local RAG Assistant)

🚀 **一个具备生产级架构、完全本地运行的检索增强生成（RAG）智能问答系统。**

本项目旨在展示如何从零串联主流 AI 技术栈，构建一个**可离线、防数据泄露、可观测且易于部署**的私有知识库问答后端。非常适合作为 AI 工程化方向的演示项目。

---

## ✨ 核心特性

- 🔒 **完全本地化**：基于 `Ollama` 驱动本地开源大模型（如 Llama 3），无需依赖外部 API。
- 📚 **多格式知识导入**：支持解析并向量化 `PDF`、`Markdown` 及 `Web 网页` 内容。
- 🧠 **长时记忆对话**：基于 `LangChain` 实现历史对话管理与代词指代消解，支持多轮追问。
- 🐳 **容器化部署**：提供多阶段构建的 `Dockerfile` 与 `docker-compose.yml`，一键拉起全套服务。
- 📊 **生产级可观测性**：内置 `Prometheus` 埋点，自动采集接口 QPS、时延与状态码，配套 `Grafana` 监控。
- ⚙️ **工程化闭环**：包含 `GitHub Actions` CI 流水线、`Locust` 性能压测脚本与 `K8s` 部署清单。

---

## 🛠️ 技术栈 (Tech Stack)

| 领域 | 核心技术 / 框架 |
| :--- | :--- |
| **模型推理** | [Ollama](https://ollama.com/) (本地模型托管), Llama 3.2 (对话), Nomic Embed (嵌入) |
| **RAG 编排** | [LangChain](https://www.langchain.com/) (逻辑链编排), PyMuPDF / BeautifulSoup (文档解析) |
| **向量存储** | [Chroma](https://www.trychroma.com/) (本地向量数据库) |
| **后端 API** | [FastAPI](https://fastapi.tiangolo.com/) (异步 Web 框架), Pydantic (数据校验) |
| **监控观测** | Prometheus (指标采集), Grafana (数据大盘) |
| **部署与交付** | Docker, Docker Compose, Kubernetes, GitHub Actions |

---

## 🚀 快速开始

### 1. 前置准备
- 安装 [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- 安装 [Ollama](https://ollama.com/) 并拉取推荐模型：
  ```bash
  ollama pull llama3.2:3b
  ollama pull nomic-embed-text
  ```

### 2. 一键启动服务
使用 Docker Compose 拉起 FastAPI 后端及监控组件：

```bash
git clone <your-repo-url>
cd local-rag-assistant
docker compose up -d --build
```

### 3. 验证服务状态
服务启动后，你可以访问以下地址：
- 📖 **API 文档 (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- 📊 **Prometheus 指标**: [http://localhost:8000/metrics](http://localhost:8000/metrics)
- 📈 **Grafana 监控面板**: [http://localhost:3000](http://localhost:3000) (默认账密: `admin`/`admin`)

---

## 💡 使用指南 (API 示例)

你可以直接在 `http://localhost:8000/docs` 页面中进行可视化测试，也可以使用以下 `cURL` 命令。

### 1. 导入知识 (URL 示例)
```bash
curl -X POST "http://127.0.0.1:8000/api/documents/upload/url" \
     -H "Content-Type: application/json" \
     -d '{"url": "https://python.langchain.com/v0.2/docs/introduction/"}'
```

### 2. 导入知识 (PDF 示例)
```bash
curl -X POST "http://127.0.0.1:8000/api/documents/upload/file" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@/path/to/your/document.pdf"
```

### 3. 基于知识库进行问答
```bash
curl -X POST "http://127.0.0.1:8000/api/chat" \
     -H "Content-Type: application/json" \
     -d '{
           "question": "What is LangChain?",
           "chat_history": []
         }'
```

---

## 🏗️ 本地开发与压测

如果你希望在宿主机直接进行开发调试：

```bash
# 1. 创建虚拟环境 (需要 Python 3.11/3.12/3.13)
python3.12 -m venv .venv
source .venv/bin/activate

# 2. 安装开发依赖
pip install -e '.[dev]'

# 3. 复制配置文件并按需修改
cp .env.example .env

# 4. 启动开发服务器
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 5. 运行性能压测 (需开新终端)
locust -f scripts/locustfile.py --host=http://127.0.0.1:8000
# 随后打开 http://localhost:8089 配置并发数
```

---

## 📁 目录结构

```text
.
├── app/                      # FastAPI 应用主目录
│   ├── api/routes/           # 路由定义 (rag.py, system.py)
│   ├── core/                 # 核心配置 (config.py)
│   ├── rag/                  # RAG 核心逻辑
│   │   ├── chain.py          # 多轮对话检索链编排
│   │   ├── loaders/          # 文档解析与分块器
│   │   └── vector_store/     # Chroma 向量库管理
│   └── schemas/              # Pydantic 数据模型
├── data/                     # 数据持久化目录 (向量库、文件)
├── deploy/                   # 部署相关配置
│   ├── docker/               # Prometheus 配置文件
│   └── k8s/                  # Kubernetes 资源清单
├── doc/                      # 规划与设计文档
├── scripts/                  # 预检、测试、压测脚本
├── tests/                    # 单元测试代码
├── Dockerfile                # 多阶段构建镜像定义
├── docker-compose.yml        # 容器编排配置
└── pyproject.toml            # 依赖与项目元数据配置
```
