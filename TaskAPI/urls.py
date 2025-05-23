"""
URL configuration for TaskAPI project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.views.generic import RedirectView


urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/v1/', include('tasks.urls')),  # Include the tasks app URLs
    path('api/v1/', include('categories.urls')),  # Include the categories app URLs
    path('api/v1/', include('comments.urls')),  # Include the comments app URLs
    path('api/v1/', include('attachments.urls')),  # Include the attachments app URLs
    path('api/v1/', include('users.urls')),  # Include the users app URLs

    path('', RedirectView.as_view(url='/api/v1/register/', permanent=False)),  # 👈 redirect root to API

    # Schema and Documentation
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]

# Use this for Local Development only and not for Production (RECOMMENDED)
if not settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)