from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import TaskModel
from .serializers import TaskSerializer
from .filters import TaskFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from .pagination import TaskPagination
from .permissions import IsOwner
from rest_framework import status


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
        parent_task = None
        # Check if the task is a subtask, then link it to a parent task
        if 'parent_task_id' in self.request.data:
            parent_task = TaskModel.objects.get(id=self.request.data['parent_task_id'])
        serializer.save(user=self.request.user, parent_task=parent_task)
    
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
    
    @action(detail=True, methods=['post'], url_path='subtasks')
    def create_subtask(self, request, pk=None):
        """
        This action allows creating a subtask for an existing task.
        """
        task = self.get_object()  # Get the parent task
        subtask_data = {
            'title': request.data.get('title'),
            'description': request.data.get('description'),
            'status': request.data.get('status', 'PENDING'),
            'priority': request.data.get('priority', 'MEDIUM'),
            'parent_task': task.id,  # Link the new task as a subtask
        }
        
        subtask_serializer = TaskSerializer(data=subtask_data)
        if subtask_serializer.is_valid():
            subtask_serializer.save(user=request.user, parent_task=task)
            return Response(subtask_serializer.data, status=status.HTTP_201_CREATED)
        return Response(subtask_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['get'], url_path='sub-tasks')
    def subtasks(self, request, pk=None):
        # Get the parent task
        parent_task = self.get_object()
        
        # Get all subtasks for this parent task
        subtasks = parent_task.subtasks.all()  # Using related_name='subtasks'
        
        # Serialize and return the subtasks
        serializer = TaskSerializer(subtasks, many=True)
        return Response(serializer.data)