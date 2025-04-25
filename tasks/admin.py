from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import TaskModel, CustomUser

class TaskModelAdmin(admin.ModelAdmin):
    """
    Custom admin interface for TaskModel.
    """
    list_display = ('user', 'title', 'created_at', 'completed', 'due_date')
    list_filter = ('priority', 'completed', 'created_at', 'due_date')
    search_fields = ('title', 'user__email', 'tags')  # Added 'user__email' for better search functionality
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')  # Making `created_at` and `updated_at` readonly
    fieldsets = (
        ('Task Details', {'fields': ('title', 'description', 'priority', 'tags', 'due_date', 'completed', 'attach_photo', 'location')}),
        ('Dates', {'fields': ('created_at', 'updated_at')}),
        ('User Information', {'fields': ('user',)}),  # Reference to CustomUser
    )
    
    # Add fields for task creation
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('user', 'title', 'description', 'due_date', 'completed', 'priority', 'tags', 'attach_photo', 'location')}
        ),
    )
# Customizing the Admin site
admin.site.site_header = "Task Management System"
admin.site.site_title = "TaskAPI"
admin.site.index_title = "Welcome to Task Management Admin"


# Register TaskModel with TaskModelAdmin
admin.site.register(TaskModel, TaskModelAdmin)