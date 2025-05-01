from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from .models import Category
from tasks.models import TaskModel
from .serializers import CategorySerializer
from tasks.serializers import TaskSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from tasks.permissions import IsOwner
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user, is_active=True)

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError({"name": "You already have a category with this name."})
        
    def destroy(self, request, *args, **kwargs):
        category_id = kwargs.get('pk')
        
        try:
            # Retrieve the category to be deleted
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return Response({"error": "Category not found."}, status=status.HTTP_404_NOT_FOUND)
        
        # Ensure the "Uncategorized" category exists
        uncategorized_category, created = Category.objects.get_or_create(
            name="Uncategorized", 
            user=category.user  # Make sure it's for the same user if needed
        )

        # Reassign tasks from the category being deleted to "Uncategorized"
        category.taskmodel_set.update(category=uncategorized_category)
        
        # Optional: You can delete the old category or mark it as inactive
        category.is_active = False  # mark inactive instead of deleting completely
        category.save()
        
        # Optional: You can fully delete the category here if needed
        # category.delete()

        # Return a success message
        return Response(
            {"message": f"Category '{category.name}' has been reassigned to 'Uncategorized'."},
            status=status.HTTP_204_NO_CONTENT
        )
    
    @action(detail=True, methods=['get'], url_path='tasks')
    def tasks(self, request, pk=None):
        category = self.get_object()
        tasks = TaskModel.objects.filter(user=request.user, category=category, is_deleted=False)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)
