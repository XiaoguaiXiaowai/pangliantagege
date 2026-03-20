from django.contrib import admin
from .models import MusicWork

@admin.register(MusicWork)
class MusicWorkAdmin(admin.ModelAdmin):
    list_display = ('title', 'work_type', 'created_at')
    list_filter = ('work_type',)
    search_fields = ('title', 'description')
