from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import TaskModel
from .serializers import TaskSerializer
from .filters import TaskFilter
from rest_framework.decorators import action

class TaskViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing, editing and deleting user tasks.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = TaskFilter
    search_fields = ['title', 'description']

    def get_queryset(self):
        return TaskModel.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        task = self.get_object()
        task.completed = True
        task.save()
        return Response({'status': 'Task marked as complete'})
