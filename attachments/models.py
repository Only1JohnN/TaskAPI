from django.db import models
from users.models import CustomUser
from tasks.models import TaskModel
from django.contrib.auth import get_user_model

User = get_user_model()


class TaskAttachment(models.Model):
    task = models.ForeignKey(TaskModel, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='task_attachments/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.task.title} - {self.file.name}"