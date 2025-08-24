from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import Announcement
from .serializers import AnnouncementSerializer
from .permissions import CanManageAnnouncements


# List announcements (filterable by batch/course)
class AnnouncementListView(generics.ListAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        qs = Announcement.objects.all().order_by("-created_at")
        batch = self.request.query_params.get("batch")
        course = self.request.query_params.get("course")

        if batch:
            qs = qs.filter(batch=batch)
        if course:
            qs = qs.filter(course=course)

        return qs

# Create manual announcements
class CreateAnnouncementView(generics.CreateAPIView):
    serializer_class = AnnouncementSerializer
    permission_classes = [CanManageAnnouncements]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

# Delete announcements
class DeleteAnnouncementView(generics.DestroyAPIView):
    permission_classes = [CanManageAnnouncements]

    def delete(self, request, pk):
        announcement = get_object_or_404(Announcement, pk=pk)
        announcement.delete()
        return Response({"detail": "Announcement deleted"}, status=status.HTTP_204_NO_CONTENT)
