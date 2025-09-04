"""
URL configuration for lms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),  # All authentication-related routes from the accounts app
    path('courses/', include('course.urls')),
    path('batches/', include('batch.urls')),
    path('content/', include('content.urls')),
    path('progress/', include('progress.urls')),
    path('api/quiz/', include('quiz.urls')),
    path('api/assignment/', include('assignment.urls')),
   path('notifications/', include('notifications.urls')),
    path('chats/',include('chats.urls')),
    path('announcements/',include('announcements.urls')),
    path('myprofile/',include('myprofile.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)