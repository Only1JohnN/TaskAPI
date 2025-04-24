from django.db import models
from users.models import CustomUser

# Create your models here.

class TaskModel(models.Model):
    """
    Model representing a task.
    """
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    due_date = models.DateTimeField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    attach_photo = models.ImageField(upload_to='task_photos/', null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    priority = models.CharField(max_length=50, choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], default='medium')
    tags = models.CharField(max_length=255, null=True, blank=True)
    
    

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Task"
        verbose_name_plural = "Tasks"
        ordering = ['-created_at']