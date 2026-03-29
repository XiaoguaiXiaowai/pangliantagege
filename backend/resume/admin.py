from django.contrib import admin
from .models import BasicInfo, Skill, TechStack, Experience, Project, Education, Certificate

@admin.register(BasicInfo)
class BasicInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'category')
    list_filter = ('category',)

@admin.register(TechStack)
class TechStackAdmin(admin.ModelAdmin):
    list_display = ('name', 'major_category', 'minor_category', 'experience', 'order')
    search_fields = ('name', 'major_category', 'minor_category')
    list_filter = ('major_category',)
    list_editable = ('order',)

@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('company', 'position', 'start_date', 'end_date', 'is_current')
    list_filter = ('is_current',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'start_date', 'end_date', 'order')
    list_editable = ('order',)

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('school', 'degree', 'major', 'start_date', 'end_date')

@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('name', 'issuer', 'date')
