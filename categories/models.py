# models.py
from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError


User = get_user_model()

class Category(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('name', 'user')  # Prevent duplicates per user

    def delete(self, *args, **kwargs):
        try:
            uncategorized_category = Category.objects.get(name="Uncategorized", user=self.user)
        except Category.DoesNotExist:
            uncategorized_category = Category.objects.create(name="Uncategorized", user=self.user)
        
        # Update all tasks in this category to "Uncategorized"
        self.taskmodel_set.update(category=uncategorized_category)

        # Optionally, mark the category as inactive or delete it
        self.is_active = False
        self.save()

    def __str__(self):
        return self.name
