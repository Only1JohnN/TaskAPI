from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        try:
            if hasattr(obj, 'user'):
                return obj.user == request.user
            elif hasattr(obj, 'task') and hasattr(obj.task, 'user'):
                return obj.task.user == request.user
            return False
        except:
            return False
