# 胖脸哥的个人网站 (PangLianTeGeGe)

👋 欢迎来到我的个人网站项目仓库！

这是一个基于 **Vue 3 + Django 5** 构建的现代化、高度定制化的个人综合网站。它不仅仅是一份枯燥的线上简历，更是我沉淀技术、展示才艺、分享工具以及与访客互动的专属数字名片。

---

## ✨ 核心特性

*   **📄 动态交互式简历 (Resume)**
    *   **瀑布流布局 (Masonry)**：技能概况与项目经历采用 CSS Multi-column 瀑布流布局，空间利用率极高，视觉紧凑。
    *   **智能走马灯 (Carousel & Marquee)**：针对长篇幅的项目描述与个人简介，实现了自动检测高度的纵向平滑滚动；对溢出的标签和职位实现了防重叠的横向跑马灯效果。
    *   **拟物化 UI 设计**：如“获得证书”模块采用带有虚线边框、渐变高亮及 SVG 勋章的“荣誉证书”卡片设计。
    *   **动态气泡背景**：基于 `requestAnimationFrame` 实现的 Luna 主题动态物理气泡背景，带有碰撞检测和边缘回弹效果。
    *   **交互联动**：鼠标悬停项目卡片时，会自动解析并高亮对应的技能栈标签。
*   **🎸 创作与才艺展示 (Talents) - *WIP***
    *   支持音频、视频作品的上传、封面展示与在线播放。
*   **💬 访客互动 (Message Board) - *WIP***
    *   无登录门槛的轻量级留言板，支持站长后台直接回复。
*   **🤖 AI 助理 (AI Assistant) - *WIP***
    *   预留第三方大模型 API 接口，提供站内智能问答互动。

## 🛠 技术栈

### 前端 (Frontend)
*   **框架**: Vue 3 (Composition API)
*   **构建工具**: Vite (rolldown-vite)
*   **路由 & 状态**: Vue Router + Pinia
*   **网络请求**: Axios
*   **样式**: 原生 CSS Modules + SASS，自定义 "Luna" (深海科技蓝) 主题色系

### 后端 (Backend)
*   **框架**: Python 3 + Django 5.x
*   **API 层**: Django REST Framework (DRF)
*   **数据库**: SQLite (开发环境) / MySQL (生产环境推荐)
*   **图像处理**: Pillow

---

## 🚀 快速启动

### 1. 克隆项目
```bash
git clone https://github.com/yourusername/pangliantagege.git
cd pangliantagege
```

### 2. 启动后端 (Django)
```bash
cd backend
# 建议使用虚拟环境
python3 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行数据库迁移
python manage.py makemigrations
python manage.py migrate

# (可选) 运行数据填充脚本，生成测试数据
python populate_db.py
python populate_techstack.py

# 启动开发服务器
python manage.py runserver
```
后端 API 将运行在 `http://127.0.0.1:8000/`。你可以通过 `http://127.0.0.1:8000/admin/` 访问后台管理面板。

### 3. 启动前端 (Vue)
```bash
# 打开一个新的终端窗口
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```
前端页面将运行在 `http://localhost:5173/` (或控制台提示的其他端口)。

---

## 📁 目录结构

```text
pangliantagege/
├── backend/                # Django 后端目录
│   ├── config/             # 项目核心配置
│   ├── resume/             # 简历模块 App
│   ├── message_board/      # 留言板模块 App
│   ├── talents/            # 才艺展示模块 App
│   ├── tools/              # 小工具模块 App
│   ├── ai_assistant/       # AI 助理模块 App
│   ├── media/              # 上传的媒体文件(头像、PDF、音乐等)
│   └── requirements.txt    # 后端依赖
├── frontend/               # Vue 3 前端目录
│   ├── src/
│   │   ├── components/     # 可复用组件 (MagicCard, Marquee等)
│   │   ├── views/          # 页面视图 (ResumeView等)
│   │   └── assets/         # 静态资源与全局样式
│   └── package.json        # 前端依赖
└── doc/                    # 项目设计文档
```

## 📄 许可证

本项目采用 [MIT License](LICENSE) 开源协议。
