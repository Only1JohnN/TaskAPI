from rest_framework import viewsets
from rest_framework.serializers import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import TaskAttachment
from .serializers import TaskAttachmentSerializer
from tasks.models import TaskModel
from tasks.permissions import IsOwner

class TaskAttachmentViewSet(viewsets.ModelViewSet):
    serializer_class = TaskAttachmentSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        task_id = self.kwargs['task_id']
        task = TaskModel.objects.filter(id=task_id, user=self.request.user).first()
        if not task:
            raise ValidationError("Task not found or access denied.")
        return TaskAttachment.objects.filter(task=task)

    def perform_create(self, serializer):
        task_id = self.kwargs['task_id']
        try:
            task = TaskModel.objects.get(id=task_id, user=self.request.user)
        except TaskModel.DoesNotExist:
            raise ValidationError("Task not found or access denied.")
        
        # Handle multiple files
        files = self.request.FILES.getlist('file')  # Get all files uploaded
        
        if not files:
            raise ValidationError("No files uploaded.")
        
        # Store each uploaded file
        for file in files:
            # Create a new attachment for each file
            TaskAttachment.objects.create(task=task, file=file)

        return Response({"message": "Attachments successfully uploaded."})