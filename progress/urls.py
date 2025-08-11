from django.urls import path
from .views import VideoProgressListView, UpdateVideoProgressView, SyllabusProgressListView, UpdateSyllabusProgressView, \
    NextVideoView, CourseSyllabusProgressListView, BatchSyllabusProgressListView, PreviousVideoView, CurrentVideoView

app_name = "progress"

urlpatterns = [
    path("my-progress/", VideoProgressListView.as_view(), name="my-progress"),
    path("update-video-progress/", UpdateVideoProgressView.as_view(), name="update-video-progress"),

    path("my-syllabus-progress/", SyllabusProgressListView.as_view(), name="my-syllabus-progress"),
    path("update-syllabus-progress/", UpdateSyllabusProgressView.as_view(), name="update-syllabus-progress"),
    path('syllabus-progress/by-course/', CourseSyllabusProgressListView.as_view(), name='course-syllabus-progress-list'),
    path('syllabus-progress/by-batch/', BatchSyllabusProgressListView.as_view(), name='batch-syllabus-progress-list'),
    path("next-video/<int:course_id>/", NextVideoView.as_view(), name="next-video"),
    path('previous-video/<int:course_id>/', PreviousVideoView.as_view(), name='previous-video'),
    path('current-video/<int:course_id>/', CurrentVideoView.as_view(), name='current-video')
]