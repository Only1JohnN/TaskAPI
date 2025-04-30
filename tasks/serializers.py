from rest_framework import serializers
from .models import TaskModel, Category, TaskAttachment, TaskComment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class TaskAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskAttachment
        fields = ['id', 'file', 'uploaded_at']

class TaskCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = TaskComment
        fields = ['id', 'user', 'comment', 'created_at']
class TaskSerializer(serializers.ModelSerializer):
    attach_photo = serializers.SerializerMethodField()
    attachments = TaskAttachmentSerializer(many=True, read_only=True)
    comments = TaskCommentSerializer(many=True, read_only=True)

    class Meta:
        model = TaskModel
        fields = [
            'id', 'title', 'description', 'created_at', 'updated_at',
            'due_date', 'completed', 'status', 'priority', 'tags', 'reminder', 'attach_photo', 'location',
            'attachments', 'comments', 'category', 'is_deleted'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_deleted', 'completed']


    def get_attach_photo(self, obj):
        if obj.attach_photo:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.attach_photo.url)
        return None