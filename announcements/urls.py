from django.urls import path
from .views import AnnouncementListView, CreateAnnouncementView, DeleteAnnouncementView

urlpatterns = [
    path("", AnnouncementListView.as_view(), name="list-announcements"),
    path("create/", CreateAnnouncementView.as_view(), name="create-announcement"),
    path("delete/<int:pk>/", DeleteAnnouncementView.as_view(), name="delete-announcement"),
]
