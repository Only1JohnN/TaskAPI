from rest_framework import serializers
from .models import TaskModel

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = ['id', 'title', 'description', 'created_at', 'updated_at', 'due_date', 'completed', 'priority', 'tags']
        read_only_fields = ['id', 'created_at', 'updated_at']