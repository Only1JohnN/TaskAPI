from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import TaskModel, Category, TaskAttachment, TaskComment
from .serializers import TaskSerializer, CategorySerializer, TaskAttachmentSerializer
from .filters import TaskFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from .pagination import TaskPagination
from .permissions import IsOwner
from rest_framework import status
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError
from rest_framework.parsers import MultiPartParser, FormParser

class TaskViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing, editing and deleting user tasks.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = TaskPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = TaskFilter
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'priority', 'created_at']

    def get_queryset(self):
        return TaskModel.objects.filter(user=self.request.user, is_deleted=False)
    

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def destroy(self, request, *args, **kwargs):
        task = self.get_object()
        task.is_deleted = True
        task.save()
        return Response({'message': 'Task moved to trash.'}, status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'])
    def trash(self, request):
        deleted_tasks = TaskModel.objects.filter(user=request.user, is_deleted=True)
        page = self.paginate_queryset(deleted_tasks)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(deleted_tasks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def restore(self, request, pk=None):
        try:
            task = TaskModel.objects.get(pk=pk, user=request.user, is_deleted=True)
        except TaskModel.DoesNotExist:
            return Response({'message': 'Task not found or not in trash.'}, status=404)

        task.is_deleted = False
        task.save()
        return Response({'message': 'Task restored successfully.'})
    
    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        task = self.get_object()
        task.completed = True
        task.save()
        return Response({'status': 'Task marked as complete'})
    
    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def add_attachment(self, request, pk=None):
        """
        Upload one or more files as attachments to a task.
        Use 'files' as the key for multiple file uploads (multipart/form-data).
        """
        task = self.get_object()
        files = request.FILES.getlist('files')  # Get list of files
    
        if not files:
            return Response({'detail': 'No files provided.'}, status=status.HTTP_400_BAD_REQUEST)
    
        attachments = []
        for file in files:
            attachment = TaskAttachment.objects.create(task=task, file=file)
            attachments.append(attachment)
    
        # Serialize all attachments
        serializer = TaskAttachmentSerializer(attachments, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['post'])
    def add_comment(self, request, pk=None):
        """
        Add a comment to a task.
        """
        task = self.get_object()
        comment_text = request.data.get('comment')
        if not comment_text:
            return Response({'detail': 'Comment text is required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the comment
        comment = TaskComment.objects.create(task=task, user=request.user, comment=comment_text)
        return Response({'id': comment.id, 'comment': comment.comment}, status=status.HTTP_201_CREATED)


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError({"name": "You already have a category with this name."})
    
    @action(detail=True, methods=['get'], url_path='tasks')
    def tasks(self, request, pk=None):
        category = self.get_object()
        tasks = TaskModel.objects.filter(user=request.user, category=category, is_deleted=False)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
