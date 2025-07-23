from django.urls import path
from .views import (
    LiveSessionListCreateView,
    LiveSessionDetailView,
    VideoListCreateView,
    VideoDetailView
)

urlpatterns = [
    path('livesessions/', LiveSessionListCreateView.as_view(), name='livesession-list-create'),
    path('livesessions/<int:pk>/', LiveSessionDetailView.as_view(), name='livesession-detail'),
    path('videos/', VideoListCreateView.as_view(), name='video-list-create'),
    path('videos/<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
]