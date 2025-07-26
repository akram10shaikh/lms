from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from .models import VideoProgress, SyllabusProgress
from content.models import Video, Syllabus
from .serializers import VideoProgressSerializer, SyllabusProgressSerializer

class VideoProgressListView(generics.ListAPIView):
    serializer_class = VideoProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VideoProgress.objects.filter(student=self.request.user)

class UpdateVideoProgressView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        video_id = request.data.get("video_id")
        watched_seconds = request.data.get("watched_seconds")

        if not video_id or watched_seconds is None:
            return Response({"error": "Missing video_id or watched_seconds."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            video = Video.objects.get(id=video_id)
        except Video.DoesNotExist:
            return Response({"error": "Video not found."}, status=status.HTTP_404_NOT_FOUND)

        progress, created = VideoProgress.objects.get_or_create(
            student=user,
            video=video,
            defaults={'watched_seconds': watched_seconds}
        )

        if not created:
            progress.watched_seconds = max(progress.watched_seconds, int(watched_seconds))
            progress.last_watched_on = timezone.now()

        if progress.watched_seconds >= int(video.duration * 0.9):
            progress.is_completed = True

        progress.save()
        return Response({"message": "Progress updated successfully."}, status=status.HTTP_200_OK)

class SyllabusProgressListView(generics.ListAPIView):
    serializer_class = SyllabusProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SyllabusProgress.objects.filter(student=self.request.user)


class UpdateSyllabusProgressView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        syllabus_id = request.data.get("syllabus_id")
        is_completed = request.data.get("is_completed", False)

        if not syllabus_id:
            return Response({"error": "Missing syllabus_id."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            syllabus = Syllabus.objects.get(id=syllabus_id)
        except Syllabus.DoesNotExist:
            return Response({"error": "Syllabus not found."}, status=status.HTTP_404_NOT_FOUND)

        progress, created = SyllabusProgress.objects.get_or_create(
            student=user,
            syllabus=syllabus,
        )

        if is_completed in [True, 'true', 'True', 1, '1']:
            progress.is_completed = True
            progress.completed_on = timezone.now()
        else:
            progress.is_completed = False
            progress.completed_on = None

        progress.save()
        return Response({"message": "Syllabus progress updated."}, status=status.HTTP_200_OK)
