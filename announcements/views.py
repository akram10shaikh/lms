from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import Announcement
from .serializers import AnnouncementSerializer
from .permissions import CanManageAnnouncements
from course.models import Course
from batch.models import Batch

# List Announcements
class AnnouncementListView(generics.ListAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = Announcement.objects.all().order_by("-created_at")

        if user.is_superuser or user.role == "admin":
            return qs

        if user.role == "student":
            batches = Batch.objects.filter(batch_students__student=user).values_list("id", flat=True)
            courses = Course.objects.filter(batches__batch_students__student=user).values_list("id", flat=True)
            return qs.filter(
                Q(batch__in=batches) |
                Q(course__in=courses) |
                (Q(batch__isnull=True) & Q(course__isnull=True))  # global
            )

        if user.role == "staff":
            batches = Batch.objects.filter(batch_staff__staff=user).values_list("id", flat=True)
            courses = Course.objects.filter(batches__batch_staff__staff=user).values_list("id", flat=True)
            return qs.filter(
                Q(batch__in=batches) |
                Q(course__in=courses) |
                (Q(batch__isnull=True) & Q(course__isnull=True))  # global
            )

        return qs.filter(batch__isnull=True, course__isnull=True)

# Create Announcements
class CreateAnnouncementView(generics.CreateAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [CanManageAnnouncements]

    def perform_create(self, serializer):
        # Ensure proper global/local handling
        batch = self.request.data.get("batch")
        course = self.request.data.get("course")

        if not batch and not course:
            serializer.save(sender=self.request.user, batch=None, course=None)
        else:
            serializer.save(sender=self.request.user)

# Update Announcements
class UpdateAnnouncementView(generics.UpdateAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated, CanManageAnnouncements]
    queryset = Announcement.objects.all()
    lookup_field = "pk"

    def perform_update(self, serializer):
        serializer.save()


# Delete Announcements
class DeleteAnnouncementView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated, CanManageAnnouncements]

    def delete(self, request, pk):
        announcement = get_object_or_404(Announcement, pk=pk)
        announcement.delete()
        return Response({"detail": "Announcement deleted"}, status=status.HTTP_204_NO_CONTENT)
