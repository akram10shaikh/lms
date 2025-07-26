from django.urls import path
from .views import VideoProgressListView, UpdateVideoProgressView, SyllabusProgressListView, UpdateSyllabusProgressView

app_name = "progress"

urlpatterns = [
    path("my-progress/", VideoProgressListView.as_view(), name="my-progress"),
    path("update-video-progress/", UpdateVideoProgressView.as_view(), name="update-video-progress"),

    path("my-syllabus-progress/", SyllabusProgressListView.as_view(), name="my-syllabus-progress"),
    path("update-syllabus-progress/", UpdateSyllabusProgressView.as_view(), name="update-syllabus-progress")
]