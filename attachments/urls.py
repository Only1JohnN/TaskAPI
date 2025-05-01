from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskAttachmentViewSet

router = DefaultRouter()
# Register the 'attachments' route for a specific task (with task_id as part of the URL)
router.register(r'tasks/(?P<task_id>\d+)/attachments', TaskAttachmentViewSet, basename='task-attachments')

urlpatterns = [
    path('', include(router.urls)),
]
