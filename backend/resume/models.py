from django.db import models

class BasicInfo(models.Model):
    name = models.CharField(max_length=100, verbose_name='姓名')
    title = models.CharField(max_length=100, verbose_name='职位/头衔')
    title_en = models.CharField(max_length=100, blank=True, null=True, verbose_name='职位/头衔(English)')
    title_ja = models.CharField(max_length=100, blank=True, null=True, verbose_name='职位/头衔(日本語)')
    gender = models.CharField(max_length=10, blank=True, null=True, verbose_name='性别', choices=(('男', '男'), ('女', '女'), ('其他', '其他')))
    age = models.IntegerField(blank=True, null=True, verbose_name='年龄')
    email = models.EmailField(verbose_name='邮箱')
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='电话')
    location = models.CharField(max_length=100, blank=True, null=True, verbose_name='所在地')
    location_en = models.CharField(max_length=100, blank=True, null=True, verbose_name='所在地(English)')
    location_ja = models.CharField(max_length=100, blank=True, null=True, verbose_name='所在地(日本語)')
    summary = models.TextField(verbose_name='个人简介(旧版)', blank=True, null=True)
    summary_en = models.TextField(verbose_name='个人简介(English)', blank=True, null=True)
    summary_ja = models.TextField(verbose_name='个人简介(日本語)', blank=True, null=True)
    summary_experience = models.TextField(verbose_name='工作经验', blank=True, null=True)
    summary_experience_en = models.TextField(verbose_name='工作经验(English)', blank=True, null=True)
    summary_experience_ja = models.TextField(verbose_name='工作经验(日本語)', blank=True, null=True)
    summary_skills = models.TextField(verbose_name='专业能力', blank=True, null=True)
    summary_skills_en = models.TextField(verbose_name='专业能力(English)', blank=True, null=True)
    summary_skills_ja = models.TextField(verbose_name='专业能力(日本語)', blank=True, null=True)
    summary_management = models.TextField(verbose_name='团队管理', blank=True, null=True)
    summary_management_en = models.TextField(verbose_name='团队管理(English)', blank=True, null=True)
    summary_management_ja = models.TextField(verbose_name='团队管理(日本語)', blank=True, null=True)
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
    category_en = models.CharField(max_length=50, blank=True, null=True, verbose_name='分类(English)')
    category_ja = models.CharField(max_length=50, blank=True, null=True, verbose_name='分类(日本語)')
    
    class Meta:
        verbose_name = '技能/关键词'
        verbose_name_plural = '技能/关键词'
        ordering = ['-level']

    def __str__(self):
        return self.name

class TechStack(models.Model):
    major_category = models.CharField(max_length=100, verbose_name='大分类', default='未分类')
    major_category_en = models.CharField(max_length=100, blank=True, null=True, verbose_name='大分类(English)')
    major_category_ja = models.CharField(max_length=100, blank=True, null=True, verbose_name='大分类(日本語)')
    minor_category = models.CharField(max_length=100, verbose_name='小分类', default='未分类')
    minor_category_en = models.CharField(max_length=100, blank=True, null=True, verbose_name='小分类(English)')
    minor_category_ja = models.CharField(max_length=100, blank=True, null=True, verbose_name='小分类(日本語)')
    name = models.CharField(max_length=100, verbose_name='技能内容')
    experience = models.CharField(max_length=50, verbose_name='经验年限', default='1年')
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name='图标(Emoji/Class)', default='⚡')
    order = models.IntegerField(default=0, verbose_name='排序')
    
    class Meta:
        verbose_name = '技术栈'
        verbose_name_plural = '技术栈'
        ordering = ['order', 'major_category', 'minor_category', 'id']

    def __str__(self):
        return f"{self.major_category} - {self.minor_category} - {self.name}"

class Experience(models.Model):
    company = models.CharField(max_length=100, verbose_name='公司/组织')
    company_en = models.CharField(max_length=100, blank=True, null=True, verbose_name='公司/组织(English)')
    company_ja = models.CharField(max_length=100, blank=True, null=True, verbose_name='公司/组织(日本語)')
    position = models.CharField(max_length=100, verbose_name='职位')
    position_en = models.CharField(max_length=100, blank=True, null=True, verbose_name='职位(English)')
    position_ja = models.CharField(max_length=100, blank=True, null=True, verbose_name='职位(日本語)')
    start_date = models.DateField(verbose_name='开始日期')
    end_date = models.DateField(blank=True, null=True, verbose_name='结束日期 (至今为空)')
    description = models.TextField(verbose_name='工作描述')
    description_en = models.TextField(blank=True, null=True, verbose_name='工作描述(English)')
    description_ja = models.TextField(blank=True, null=True, verbose_name='工作描述(日本語)')
    is_current = models.BooleanField(default=False, verbose_name='至今')

    class Meta:
        verbose_name = '工作经历'
        verbose_name_plural = '工作经历'
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.company} - {self.position}"

class Project(models.Model):
    name = models.CharField(max_length=100, verbose_name='项目名称')
    name_en = models.CharField(max_length=100, blank=True, null=True, verbose_name='项目名称(English)')
    name_ja = models.CharField(max_length=100, blank=True, null=True, verbose_name='项目名称(日本語)')
    role = models.CharField(max_length=100, verbose_name='担任角色')
    role_en = models.CharField(max_length=100, blank=True, null=True, verbose_name='担任角色(English)')
    role_ja = models.CharField(max_length=100, blank=True, null=True, verbose_name='担任角色(日本語)')
    start_date = models.DateField(blank=True, null=True, verbose_name='开始日期')
    end_date = models.DateField(blank=True, null=True, verbose_name='结束日期')
    description = models.TextField(verbose_name='项目描述(旧版)', blank=True, null=True)
    description_en = models.TextField(verbose_name='项目描述(English)', blank=True, null=True)
    description_ja = models.TextField(verbose_name='项目描述(日本語)', blank=True, null=True)
    bg_description = models.TextField(verbose_name='项目背景', blank=True, null=True)
    bg_description_en = models.TextField(verbose_name='项目背景(English)', blank=True, null=True)
    bg_description_ja = models.TextField(verbose_name='项目背景(日本語)', blank=True, null=True)
    duty_description = models.TextField(verbose_name='项目职责', blank=True, null=True)
    duty_description_en = models.TextField(verbose_name='项目职责(English)', blank=True, null=True)
    duty_description_ja = models.TextField(verbose_name='项目职责(日本語)', blank=True, null=True)
    solution_description = models.TextField(verbose_name='解决方案', blank=True, null=True)
    solution_description_en = models.TextField(verbose_name='解决方案(English)', blank=True, null=True)
    solution_description_ja = models.TextField(verbose_name='解决方案(日本語)', blank=True, null=True)
    result_description = models.TextField(verbose_name='项目成果', blank=True, null=True)
    result_description_en = models.TextField(verbose_name='项目成果(English)', blank=True, null=True)
    result_description_ja = models.TextField(verbose_name='项目成果(日本語)', blank=True, null=True)
    technologies = models.CharField(max_length=200, blank=True, null=True, verbose_name='使用技术')
    link = models.URLField(blank=True, null=True, verbose_name='项目链接')
    order = models.IntegerField(default=0, verbose_name='显示顺序(从小到大)')

    class Meta:
        verbose_name = '项目经历'
        verbose_name_plural = '项目经历'
        ordering = ['order', '-start_date']

    def __str__(self):
        return self.name

class Education(models.Model):
    school = models.CharField(max_length=100, verbose_name='学校')
    school_en = models.CharField(max_length=100, blank=True, null=True, verbose_name='学校(English)')
    school_ja = models.CharField(max_length=100, blank=True, null=True, verbose_name='学校(日本語)')
    degree = models.CharField(max_length=100, verbose_name='学位')
    degree_en = models.CharField(max_length=100, blank=True, null=True, verbose_name='学位(English)')
    degree_ja = models.CharField(max_length=100, blank=True, null=True, verbose_name='学位(日本語)')
    major = models.CharField(max_length=100, verbose_name='专业')
    major_en = models.CharField(max_length=100, blank=True, null=True, verbose_name='专业(English)')
    major_ja = models.CharField(max_length=100, blank=True, null=True, verbose_name='专业(日本語)')
    start_date = models.DateField(verbose_name='开始日期')
    end_date = models.DateField(blank=True, null=True, verbose_name='结束日期')

    class Meta:
        verbose_name = '教育背景'
        verbose_name_plural = '教育背景'
        ordering = ['-start_date']

    def __str__(self):
        return self.school

class Certificate(models.Model):
    name = models.CharField(max_length=100, verbose_name='证书名称')
    name_en = models.CharField(max_length=100, blank=True, null=True, verbose_name='证书名称(English)')
    name_ja = models.CharField(max_length=100, blank=True, null=True, verbose_name='证书名称(日本語)')
    issuer = models.CharField(max_length=100, verbose_name='颁发机构')
    issuer_en = models.CharField(max_length=100, blank=True, null=True, verbose_name='颁发机构(English)')
    issuer_ja = models.CharField(max_length=100, blank=True, null=True, verbose_name='颁发机构(日本語)')
    date = models.DateField(verbose_name='颁发日期')
    link = models.URLField(blank=True, null=True, verbose_name='证书链接')

    class Meta:
        verbose_name = '证书'
        verbose_name_plural = '证书'
        ordering = ['-date']

    def __str__(self):
        return self.name
