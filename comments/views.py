from rest_framework import viewsets
from rest_framework.serializers import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import TaskComment
from .serializers import TaskCommentSerializer
from tasks.models import TaskModel
from rest_framework.decorators import action
from tasks.permissions import IsOwner

class TaskCommentViewSet(viewsets.ModelViewSet):
    serializer_class = TaskCommentSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        task = TaskModel.objects.filter(id=task_id, user=self.request.user).first()
        if not task:
            raise ValidationError("Task not found or access denied.")
        return TaskComment.objects.filter(task=task)

    def perform_create(self, serializer):
        task_id = self.kwargs['task_id']
        try:
            task = TaskModel.objects.get(id=task_id, user=self.request.user)
        except TaskModel.DoesNotExist:
            raise ValidationError("Task not found or access denied.")
        serializer.save(user=self.request.user, task=task)

    @action(detail=True, methods=['get'], url_path='comments')
    def task_comments(self, request, pk=None):
        """
        Get all comments for a specific task.
        """
        task = self.get_object()  # Get the task using the pk (primary key)
        comments = TaskComment.objects.filter(task=task, user=request.user)
        serializer = TaskCommentSerializer(comments, many=True)
        return Response(serializer.data)
