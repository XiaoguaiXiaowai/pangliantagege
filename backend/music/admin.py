from django.contrib import admin
from .models import MusicWork


def _en(field):
    """某字段的 English 变体字段名"""
    return (f'{field}_en',)


def _ja(field):
    """某字段的日本語变体字段名"""
    return (f'{field}_ja',)


@admin.register(MusicWork)
class MusicWorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'work_type', 'created_at')
    list_filter = ('work_type',)
    search_fields = ('title', 'description', 'title_en', 'title_ja')
    fieldsets = (
        (None, {
            'fields': ('work_type', 'cover_image', 'audio_file', 'video_file', 'video_url')
        }),
        ('中文', {'fields': ('title', 'description')}),
        ('English', {'fields': _en('title') + _en('description'), 'classes': ('wide',)}),
        ('日本語', {'fields': _ja('title') + _ja('description'), 'classes': ('wide',)}),
    )