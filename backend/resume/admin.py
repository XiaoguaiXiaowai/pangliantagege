from django.contrib import admin
from .models import BasicInfo, Skill, TechStack, Experience, Project, Education, Certificate


def _en(field):
    """某字段的 English 变体字段名"""
    return (f'{field}_en',)


def _ja(field):
    """某字段的日本語变体字段名"""
    return (f'{field}_ja',)


def _lang_fieldsets(main_fields, zh_fields, en_fields, ja_fields):
    """按 中文 / English / 日本語 分组多语言字段（各组字段互不重叠）"""
    return (
        (None, {'fields': main_fields}),
        ('中文', {'fields': zh_fields}),
        ('English', {'fields': en_fields, 'classes': ('wide',)}),
        ('日本語', {'fields': ja_fields, 'classes': ('wide',)}),
    )


@admin.register(BasicInfo)
class BasicInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'title', 'email')
    fieldsets = _lang_fieldsets(
        main_fields=('name', 'gender', 'age', 'email', 'phone', 'avatar'),
        zh_fields=('title', 'location', 'summary', 'summary_experience', 'summary_skills', 'summary_management'),
        en_fields=_en('title') + _en('location') + _en('summary') + _en('summary_experience') + _en('summary_skills') + _en('summary_management'),
        ja_fields=_ja('title') + _ja('location') + _ja('summary') + _ja('summary_experience') + _ja('summary_skills') + _ja('summary_management'),
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'level', 'category')
    list_filter = ('category',)
    fieldsets = _lang_fieldsets(
        main_fields=('name', 'level'),
        zh_fields=('category',),
        en_fields=_en('category'),
        ja_fields=_ja('category'),
    )


@admin.register(TechStack)
class TechStackAdmin(admin.ModelAdmin):
    list_display = ('name', 'major_category', 'minor_category', 'experience', 'order')
    search_fields = ('name', 'major_category', 'minor_category')
    list_filter = ('major_category',)
    list_editable = ('order',)
    fieldsets = _lang_fieldsets(
        main_fields=('name', 'icon', 'experience', 'order'),
        zh_fields=('major_category', 'minor_category'),
        en_fields=_en('major_category') + _en('minor_category'),
        ja_fields=_ja('major_category') + _ja('minor_category'),
    )


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('company', 'position', 'start_date', 'end_date', 'is_current')
    list_filter = ('is_current',)
    fieldsets = _lang_fieldsets(
        main_fields=('company', 'position', 'start_date', 'end_date', 'is_current'),
        zh_fields=('description',),
        en_fields=_en('company') + _en('position') + _en('description'),
        ja_fields=_ja('company') + _ja('position') + _ja('description'),
    )


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'start_date', 'end_date', 'order')
    list_editable = ('order',)
    fieldsets = _lang_fieldsets(
        main_fields=('name', 'role', 'start_date', 'end_date', 'technologies', 'link', 'order'),
        zh_fields=('description', 'bg_description', 'duty_description', 'solution_description', 'result_description'),
        en_fields=_en('name') + _en('role') + _en('description') + _en('bg_description') + _en('duty_description') + _en('solution_description') + _en('result_description'),
        ja_fields=_ja('name') + _ja('role') + _ja('description') + _ja('bg_description') + _ja('duty_description') + _ja('solution_description') + _ja('result_description'),
    )


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('school', 'degree', 'major', 'start_date', 'end_date')
    fieldsets = _lang_fieldsets(
        main_fields=('start_date', 'end_date'),
        zh_fields=('school', 'degree', 'major'),
        en_fields=_en('school') + _en('degree') + _en('major'),
        ja_fields=_ja('school') + _ja('degree') + _ja('major'),
    )


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = ('name', 'issuer', 'date')
    fieldsets = _lang_fieldsets(
        main_fields=('date', 'link'),
        zh_fields=('name', 'issuer'),
        en_fields=_en('name') + _en('issuer'),
        ja_fields=_ja('name') + _ja('issuer'),
    )