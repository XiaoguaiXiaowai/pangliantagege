import os
import django
from datetime import date

# 设置 Django 环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from resume.models import BasicInfo, Skill, TechStack, Experience, Project, Education, Language, Certificate

def populate():
    print("开始填充示例数据...")

    # Basic Info
    if not BasicInfo.objects.exists():
        BasicInfo.objects.create(
            name="李佳",
            title="全栈开发工程师",
            email="lijia@example.com",
            phone="13800138000",
            location="北京",
            summary="热爱编程，擅长 Python 和 Vue，拥有丰富的 Web 开发经验。致力于构建优雅、高效的用户体验。",
        )
        print("已创建基本信息")

    # Skills (Keywords)
    if not Skill.objects.exists():
        # Soft Skills / Strengths
        Skill.objects.create(name="团队协作", level=90, category="Strength")
        Skill.objects.create(name="快速学习", level=95, category="Strength")
        Skill.objects.create(name="问题解决", level=85, category="Strength")
        
        # Hobbies
        Skill.objects.create(name="摄影", level=60, category="Hobby")
        Skill.objects.create(name="徒步", level=70, category="Hobby")
        Skill.objects.create(name="科幻阅读", level=80, category="Hobby")
        
        # Roles
        Skill.objects.create(name="全栈开发", level=90, category="Role")
        Skill.objects.create(name="技术博主", level=75, category="Role")
        
        # Tech Keywords (for Marquee, simpler version)
        Skill.objects.create(name="Python", level=90, category="Backend")
        Skill.objects.create(name="Vue.js", level=80, category="Frontend")
        
        print("已创建关键词数据")

    # Tech Stack (Detailed)
    if not TechStack.objects.exists():
        TechStack.objects.create(name="Python", years=5, icon="🐍")
        TechStack.objects.create(name="Django", years=4, icon="🎸")
        TechStack.objects.create(name="Vue.js", years=3, icon="💚")
        TechStack.objects.create(name="JavaScript", years=4, icon="📜")
        TechStack.objects.create(name="Docker", years=2, icon="🐳")
        TechStack.objects.create(name="Elasticsearch", years=2, icon="🔍")
        print("已创建技术栈数据")

    # Experience
    if not Experience.objects.exists():
        Experience.objects.create(
            company="某知名互联网公司",
            position="高级开发工程师",
            start_date=date(2023, 1, 1),
            is_current=True,
            description="负责公司核心业务系统的后端架构设计与开发，主导了从单体应用向微服务架构的迁移。"
        )
        Experience.objects.create(
            company="初创科技公司",
            position="Web 开发工程师",
            start_date=date(2020, 6, 1),
            end_date=date(2022, 12, 31),
            description="独立完成了公司官网及后台管理系统的前后端开发，使用了 Django 和 Vue 技术栈。"
        )
        print("已创建工作经历")

    # Projects
    if not Project.objects.exists():
        Project.objects.create(
            name="个人知识库系统",
            role="独立开发者",
            start_date=date(2024, 1, 1),
            description="一个基于 Markdown 的个人知识管理系统，支持全文检索和 AI 辅助写作。",
            technologies="Python, Django, Elasticsearch, Vue.js",
            link="https://github.com/example/knowledge-base"
        )
        print("已创建项目经历")

    # Education
    if not Education.objects.exists():
        Education.objects.create(
            school="北京某大学",
            degree="本科",
            major="计算机科学与技术",
            start_date=date(2016, 9, 1),
            end_date=date(2020, 6, 30)
        )
        print("已创建教育背景")

    # Languages
    if not Language.objects.exists():
        Language.objects.create(name="中文", proficiency="母语")
        Language.objects.create(name="英语", proficiency="流利 (CET-6)")
        print("已创建语言能力")

    # Certificates
    if not Certificate.objects.exists():
        Certificate.objects.create(
            name="AWS 认证解决方案架构师",
            issuer="Amazon Web Services",
            date=date(2023, 5, 15)
        )
        Certificate.objects.create(
            name="PMP 项目管理专业人士",
            issuer="PMI",
            date=date(2022, 10, 20)
        )
        print("已创建证书")

    print("数据填充完成！")

if __name__ == '__main__':
    populate()
