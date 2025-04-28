from rest_framework import serializers
from .models import TaskModel

class TaskSerializer(serializers.ModelSerializer):
    attach_photo = serializers.SerializerMethodField()

    class Meta:
        model = TaskModel
        fields = [
            'id', 'title', 'description', 'created_at', 'updated_at',
            'due_date', 'completed', 'priority', 'tags', 'attach_photo', 'location'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


    def get_attach_photo(self, obj):
        if obj.attach_photo:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.attach_photo.url)
        return None