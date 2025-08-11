from django.urls import path
from .views import (
    LiveSessionListCreateView,
    LiveSessionDetailView,
    VideoListCreateView,
    VideoDetailView, CourseSyllabusWithVideosView, SyllabusContentView, VideoNavigationView
)

urlpatterns = [
    path('livesessions/', LiveSessionListCreateView.as_view(), name='livesession-list-create'),
    path('livesessions/<int:pk>/', LiveSessionDetailView.as_view(), name='livesession-detail'),
    path('videos/', VideoListCreateView.as_view(), name='video-list-create'),
    path('videos/<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
    path('syllabus-with-videos/<int:course_id>/', CourseSyllabusWithVideosView.as_view(), name='syllabus-with-videos'),
    path('syllabus-with-content/<int:course_id>/', SyllabusContentView.as_view(), name='syllabus-with-content'),
    path('video-navigation/<int:course_id>/<int:video_id>/', VideoNavigationView.as_view(), name='video-navigation'),
]