# notifications/urls.py

from django.urls import path
from .views import (
    NotificationListView,
    MarkNotificationReadView,
    AdminSendNotificationView,
    StaffSendBatchNotificationView,
)

urlpatterns = [
    path("", NotificationListView.as_view(), name="list-notifications"),
    path("<int:pk>/mark-read/", MarkNotificationReadView.as_view(), name="mark-notification-read"),
    path("admin/send/", AdminSendNotificationView.as_view(), name="admin-send-notification"),
    path("staff/send-batch/", StaffSendBatchNotificationView.as_view(), name="staff-send-batch-notification"),
]
