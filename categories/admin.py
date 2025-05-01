# admin.py
from django.contrib import admin
from django.core.exceptions import ValidationError
from .models import Category

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'user', 'created_at')
    search_fields = ('name', 'user__email')
    readonly_fields = ('created_at',)
    ordering = ('name',)

    def delete_model(self, request, obj):
        if obj.taskmodel_set.exists():
            raise ValidationError("This category is still in use by tasks. Please reassign or mark as inactive.")
        super().delete_model(request, obj)