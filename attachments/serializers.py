from rest_framework import serializers
from .models import TaskAttachment

class TaskAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAttachment
        fields = ['id', 'task', 'file', 'uploaded_at']
        read_only_fields = ['id', 'task', 'uploaded_at']

    file = serializers.FileField()
