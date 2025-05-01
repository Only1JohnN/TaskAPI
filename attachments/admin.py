from django.contrib import admin
from .models import TaskAttachment

@admin.register(TaskAttachment)
class TaskAttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'file', 'uploaded_at')
    search_fields = ('task__title',)
    readonly_fields = ('uploaded_at',)
    ordering = ('-uploaded_at',)
