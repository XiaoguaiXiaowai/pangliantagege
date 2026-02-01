from django.db import models

class BasicInfo(models.Model):
    name = models.CharField(max_length=100, verbose_name='姓名')
    title = models.CharField(max_length=100, verbose_name='职位/头衔')
    email = models.EmailField(verbose_name='邮箱')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='电话')
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name='所在地')
    summary = models.TextField(verbose_name='个人简介')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name='头像')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = '基本信息'
        verbose_name_plural = '基本信息'

    def __str__(self):
        return self.name

class Skill(models.Model):
    name = models.CharField(max_length=50, verbose_name='技能名称')
    level = models.IntegerField(default=50, verbose_name='熟练度(0-100)')
    category = models.CharField(max_length=50, blank=True, null=True, verbose_name='分类') # e.g. Frontend, Backend, Tools
    
    class Meta:
        verbose_name = '技能/关键词'
        verbose_name_plural = '技能/关键词'
        ordering = ['-level']

    def __str__(self):
        return self.name

class TechStack(models.Model):
    name = models.CharField(max_length=50, verbose_name='技术名称')
    years = models.IntegerField(default=1, verbose_name='经验年限(年)')
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name='图标(Emoji/Class)', default='⚡')
    
    class Meta:
        verbose_name = '技术栈'
        verbose_name_plural = '技术栈'
        ordering = ['-years']

    def __str__(self):
        return self.name

class Experience(models.Model):
    company = models.CharField(max_length=100, verbose_name='公司/组织')
    position = models.CharField(max_length=100, verbose_name='职位')
    start_date = models.DateField(verbose_name='开始日期')
    end_date = models.DateField(blank=True, null=True, verbose_name='结束日期 (至今为空)')
    description = models.TextField(verbose_name='工作描述')
    is_current = models.BooleanField(default=False, verbose_name='至今')

    class Meta:
        verbose_name = '工作经历'
        verbose_name_plural = '工作经历'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.company} - {self.position}"

class Project(models.Model):
    name = models.CharField(max_length=100, verbose_name='项目名称')
    role = models.CharField(max_length=100, verbose_name='担任角色')
    start_date = models.DateField(blank=True, null=True, verbose_name='开始日期')
    end_date = models.DateField(blank=True, null=True, verbose_name='结束日期')
    description = models.TextField(verbose_name='项目描述')
    technologies = models.CharField(max_length=200, blank=True, null=True, verbose_name='使用技术')
    link = models.URLField(blank=True, null=True, verbose_name='项目链接')

    class Meta:
        verbose_name = '项目经历'
        verbose_name_plural = '项目经历'
        ordering = ['-start_date']

    def __str__(self):
        return self.name

class Education(models.Model):
    school = models.CharField(max_length=100, verbose_name='学校')
    degree = models.CharField(max_length=100, verbose_name='学位')
    major = models.CharField(max_length=100, verbose_name='专业')
    start_date = models.DateField(verbose_name='开始日期')
    end_date = models.DateField(blank=True, null=True, verbose_name='结束日期')

    class Meta:
        verbose_name = '教育背景'
        verbose_name_plural = '教育背景'
        ordering = ['-start_date']

    def __str__(self):
        return self.school

class Language(models.Model):
    name = models.CharField(max_length=50, verbose_name='语言')
    proficiency = models.CharField(max_length=50, verbose_name='熟练程度') # e.g. Native, Fluent, Intermediate

    class Meta:
        verbose_name = '语言能力'
        verbose_name_plural = '语言能力'

    def __str__(self):
        return self.name

class Certificate(models.Model):
    name = models.CharField(max_length=100, verbose_name='证书名称')
    issuer = models.CharField(max_length=100, verbose_name='颁发机构')
    date = models.DateField(verbose_name='颁发日期')
    link = models.URLField(blank=True, null=True, verbose_name='证书链接')

    class Meta:
        verbose_name = '证书'
        verbose_name_plural = '证书'
        ordering = ['-date']

    def __str__(self):
        return self.name
