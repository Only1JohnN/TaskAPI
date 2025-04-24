from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework import status
from .models import TaskModel
from .serializers import TaskSerializer
from .filters import TaskFilter

class TaskListCreateView(ListCreateAPIView):
    """
    View to list and create tasks.
    """
    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = TaskFilter
    # search_fields = ['title', 'description']  # Specify the fields you want to search by

    def get_queryset(self):
        # Only return tasks for the currently authenticated user
        return TaskModel.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Attach the user automatically when creating a task
        serializer.save(user=self.request.user)



class TaskDetailView(RetrieveUpdateDestroyAPIView):
    """
    View to retrieve, update or delete a task.
    """
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return TaskModel.objects.filter(user=self.request.user)

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        task = self.get_object()
        serializer = self.get_serializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        task = self.get_object()
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
