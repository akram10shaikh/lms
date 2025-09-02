from django.urls import path
from .views import (
    AnnouncementListView,
    CreateAnnouncementView,
    UpdateAnnouncementView,
    DeleteAnnouncementView,
)

urlpatterns = [
    path("", AnnouncementListView.as_view(), name="list-announcements"),
    path("create/", CreateAnnouncementView.as_view(), name="create-announcement"),
    path("update/<int:pk>/", UpdateAnnouncementView.as_view(), name="update-announcement"),
    path("delete/<int:pk>/", DeleteAnnouncementView.as_view(), name="delete-announcement"),
]
