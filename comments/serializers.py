from rest_framework import serializers
from .models import TaskComment

class TaskCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComment
        fields = ['id', 'task', 'user', 'comment', 'created_at']
        read_only_fields = ['id', 'task', 'user', 'created_at']
