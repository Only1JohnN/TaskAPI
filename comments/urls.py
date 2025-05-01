from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskCommentViewSet

router = DefaultRouter()
router.register(r'tasks/(?P<task_id>\d+)/comments', TaskCommentViewSet, basename='task-comments')

urlpatterns = [
    path('', include(router.urls)),
]
