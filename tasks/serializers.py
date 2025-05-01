from rest_framework import serializers
from .models import TaskModel
from comments.serializers import TaskCommentSerializer
from attachments.serializers import TaskAttachmentSerializer

class TaskSerializer(serializers.ModelSerializer):
    attach_photo = serializers.SerializerMethodField()
    attachments = TaskAttachmentSerializer(many=True, read_only=True)
    comments = TaskCommentSerializer(many=True, read_only=True)
    subtasks = serializers.SerializerMethodField()

    class Meta:
        model = TaskModel
        fields = [
            'id', 'parent_task', 'title', 'description', 'created_at', 'updated_at',
            'due_date', 'completed', 'status', 'priority', 'tags', 'reminder',
            'attach_photo', 'location', 'attachments', 'comments', 'category',
            'is_deleted', 'subtasks'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_deleted', 'completed']

    def get_attach_photo(self, obj):
        if obj.attach_photo:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.attach_photo.url)
        return None

    def get_subtasks(self, obj):
        subtasks = obj.subtasks.filter(is_deleted=False)
        serializer = TaskSerializer(subtasks, many=True, context=self.context)
        return serializer.data