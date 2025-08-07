
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , AllowAny
from .models import Notification, NotificationPreference
from .serializers import (
    NotificationSerializer,
    NotificationPreferenceSerializer,
    SendNotificationSerializer
)
from accounts.permissions import IsAdmin, IsStaff
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings

User = get_user_model()

# 1. List Notifications for Logged-in User
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')


# 2. Mark a Notification as Read
class MarkNotificationReadView(generics.UpdateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]
    queryset = Notification.objects.all()

    def update(self, request, *args, **kwargs):
        notification = self.get_object()
        if notification.user != request.user:
            return Response({"detail": "Unauthorized"}, status=403)

        notification.is_read = True
        notification.save()
        return Response({"message": "Notification marked as read."}, status=200)


# 3. Get or Update Notification Preferences
class NotificationPreferenceView(generics.RetrieveUpdateAPIView):
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj, _ = NotificationPreference.objects.get_or_create(user=self.request.user)
        return obj


# 4. Admin: Send platform-wide notification to all users
class AdminSendNotificationView(generics.CreateAPIView):
    serializer_class = SendNotificationSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.validated_data['message']

        users = User.objects.all()
        notifications = []
        email_list = []

        for user in users:
            Notification.objects.create(user=user, message=message)

            # Check notification preference
            preference, _ = NotificationPreference.objects.get_or_create(user=user)
            if preference.email_notifications:
                email_list.append(user.email)

        if email_list:
            send_mail(
                subject="New Platform Notification",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=email_list,
                fail_silently=True
            )

        return Response({"message": f"Notification sent to {users.count()} users."}, status=status.HTTP_201_CREATED)


# 5. Staff: Send batch-specific notification (stub logic for batch filtering)
class StaffSendBatchNotificationView(generics.CreateAPIView):
    serializer_class = SendNotificationSerializer
    permission_classes = [IsAuthenticated, IsStaff]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        message = serializer.validated_data['message']

        # TODO: Replace this with real logic based on batch filtering
        batch_users = User.objects.filter(is_staff=False)  # Example only

        notifications = []
        email_list = []

        for user in batch_users:
            Notification.objects.create(user=user, message=message)
            preference, _ = NotificationPreference.objects.get_or_create(user=user)
            if preference.email_notifications:
                email_list.append(user.email)

        if email_list:
            send_mail(
                subject="New Batch Notification",
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=email_list,
                fail_silently=True
            )

        return Response({"message": f"Batch notification sent to {batch_users.count()} users."}, status=status.HTTP_201_CREATED)
