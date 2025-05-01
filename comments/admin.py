from django.contrib import admin
from .models import TaskComment

@admin.register(TaskComment)
class TaskCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'user', 'comment', 'created_at')
    search_fields = ('comment', 'task__title', 'user__email')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
