from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'



    def ready(self):
        # Lazy import inside ready()
        from drf_spectacular.openapi import AutoSchema
        from rest_framework.views import APIView
        APIView.schema = AutoSchema()