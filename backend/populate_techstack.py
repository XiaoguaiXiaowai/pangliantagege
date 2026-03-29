import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from resume.models import TechStack

data = [
    ("一、云计算与基础设施", "1.云平台", "AWS（核心）", "8年"),
    ("一、云计算与基础设施", "1.云平台", "阿里云", "2年"),
    ("一、云计算与基础设施", "2.容器与编排", "Docker", "1年"),
    ("一、云计算与基础设施", "2.容器与编排", "K3s（轻量级 Kubernetes）", "1年"),
    ("一、云计算与基础设施", "3.基础设施即代码（IaC）", "Terraform（通过 Trae 工具集成）", "1年"),
    ("一、云计算与基础设施", "4.监控与告警", "Zabbix", "8年"),
    ("一、云计算与基础设施", "4.监控与告警", "Amazon CloudWatch", "8年"),
    ("一、云计算与基础设施", "4.监控与告警", "Prometheus + Grafana", "1年"),
    ("一、云计算与基础设施", "5.任务调度", "Jobarranger", "8年"),
    
    ("二、数据与数据库", "1.关系型数据库", "MySQL、Amazon Aurora", "10年+"),
    ("二、数据与数据库", "1.关系型数据库", "Oracle", "10年+"),
    ("二、数据与数据库", "1.关系型数据库", "PostgreSQL", "4年"),
    ("二、数据与数据库", "2.数据仓库", "Amazon Redshift", "8年"),
    ("二、数据与数据库", "3.消息队列", "Amazon SQS", "8年"),
    ("二、数据与数据库", "4.大数据查询", "Amazon Athena", "6年"),
    
    ("三、数据工程与 BI", "1.ETL 工具", "Talend", "8年"),
    ("三、数据工程与 BI", "1.ETL 工具", "AWS Glue", "6年"),
    ("三、数据工程与 BI", "2.BI 可视化", "Tableau", "6年"),
    ("三、数据工程与 BI", "2.BI 可视化", "Power BI", "1年"),
    ("三、数据工程与 BI", "3.数据架构", "DWH/BI 系统集群设计与优化", "8年"),
    
    ("四、Web 应用开发", "1.语言", "JAVA", "10年+"),
    ("四、Web 应用开发", "1.语言", "Python", "10年+"),
    ("四、Web 应用开发", "2.框架", "Spring", "8年"),
    ("四、Web 应用开发", "2.框架", "Spring Boot", "4年"),
    ("四、Web 应用开发", "2.框架", "Django", "1年"),
    ("四、Web 应用开发", "2.框架", "Vue.js", "1年"),
    ("四、Web 应用开发", "3.页面技术", "JSP（历史项目）", "8年"),
    ("四、Web 应用开发", "4.全栈能力", "独立完成前后端开发、数据库设计、部署全流程", "1年"),
    
    ("五、AI 与智能应用", "1.大模型（LLM）", "Llama3、Mistral、Gemini-3.1、GPT-5.3（用于辅助开发）", "1年"),
    ("五、AI 与智能应用", "2.RAG 技术", "LangChain、Chroma（向量数据库）、BGE 嵌入模型", "1年"),
    ("五、AI 与智能应用", "3.本地 AI 部署", "Ollama（MacOS M1 架构）", "1年"),
    ("五、AI 与智能应用", "4.AI 开发模式", "Trae + LLM 辅助编程", "1年"),
    
    ("六、DevOps 自动化", "1.CI/CD", "GitHub Actions（自动化测试、构建、部署）", "1年"),
    ("六、DevOps 自动化", "2.版本控制", "Git", "8年"),
    ("六、DevOps 自动化", "3.部署环境", "Amazon linux、Ubuntu、Redhat", "8年"),
    ("六、DevOps 自动化", "4.自动化脚本", "Linux Shell、Python、VBA", "8年"),
    
    ("七、方法论与软技能", "1.项目管理", "中小规模项目（5-12人团队）全周期管理、预算控制", "10年+"),
    ("七、方法论与软技能", "2.运维理念", "SRE（站点可靠性工程）、故障分级响应、根因分析（RCA）", "8年"),
    ("七、方法论与软技能", "3.流程优化", "体系化监控、标准化解决方案模板", "8年"),
    ("七、方法论与软技能", "3.流程优化", "敏捷开发", "2年"),
    ("七、方法论与软技能", "4.外语能力", "日语（流利，可直接对日方客提案）", "10年+"),
    ("七、方法论与软技能", "4.外语能力", "英语（读写流利，口语可基础交流）", "10年+"),
]

TechStack.objects.all().delete()

for idx, (major, minor, name, exp) in enumerate(data):
    TechStack.objects.create(
        major_category=major,
        minor_category=minor,
        name=name,
        experience=exp,
        order=idx
    )

print("TechStack data populated successfully!")
