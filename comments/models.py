from django.db import models
from users.models import CustomUser
from tasks.models import TaskModel
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskComment(models.Model):
    task = models.ForeignKey(TaskModel, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)