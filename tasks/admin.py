from django.contrib import admin
from .models import TaskModel

class TaskModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'created_at', 'completed', 'due_date')
    list_filter = ('priority', 'completed', 'created_at', 'due_date')
    search_fields = ('title', 'user__email', 'tags')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Task Details', {
            'fields': ('title', 'description', 'priority', 'tags', 'due_date', 'completed', 'attach_photo', 'location')
        }),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
        ('User Information', {'fields': ('user',)}),
    )

# Customize admin site branding
admin.site.site_header = "Task Management System"
admin.site.site_title = "TaskAPI"
admin.site.index_title = "Welcome to Task Management Admin"

admin.site.register(TaskModel, TaskModelAdmin)
