from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework.views import APIView

from batch.models import BatchStudent
from course.models import Enrollment, Course
from .models import LiveSession, Video, Syllabus
from .serializers import LiveSessionSerializer, VideoSerializer, SyllabusWithVideosSerializer, \
    SyllabusWithContentSerializer, VideoMiniSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsStaffOrReadOnly
from course.utils import is_user_enrolled

# LiveSession Views (with batch filtering + permission)
class LiveSessionListCreateView(generics.ListCreateAPIView):
    serializer_class = LiveSessionSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        queryset = LiveSession.objects.all()
        batch_id = self.request.query_params.get('batch')
        user = self.request.user
        if batch_id:
            queryset = queryset.filter(batch_id=batch_id)
            # Restriction for student. They can only see sessions from batches they belong to
            if user.is_authenticated and user.role == 'student':
                from batch.models import BatchStudent  # avoid circular import
                if not BatchStudent.objects.filter(student=user, batch_id=batch_id).exists():
                    return LiveSession.objects.none()

        return queryset

class LiveSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LiveSession.objects.all()
    serializer_class = LiveSessionSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_object(self):
        obj = super().get_object()
        user = self.request.user

        # Allow access if admin or staff
        if user.is_staff or user.role in ['admin', 'staff']:
            return obj

        # Allow access if student is enrolled in the batch
        if user.role == 'student':
            is_enrolled = BatchStudent.objects.filter(student=user, batch=obj.batch).exists()
            if is_enrolled:
                return obj
            else:
                raise PermissionDenied("You are not enrolled in this batch.")

        raise PermissionDenied("You do not have permission to access this LiveSession.")


# Video Views (with course filtering + permission)
class VideoListCreateView(generics.ListCreateAPIView):
    serializer_class = VideoSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        queryset = Video.objects.all()
        course_id = self.request.query_params.get('course')
        user = self.request.user
        if course_id:
            queryset = queryset.filter(course_id=course_id)

            # Restriction for student if not enrolled
            if user.is_authenticated and user.role == 'student':
                from course.models import Course  # Import here to avoid circular import
                try:
                    course = Course.objects.get(id=course_id)
                except Course.DoesNotExist:
                    return Video.objects.none()

                if not is_user_enrolled(user, course):
                    return Video.objects.none()

        return queryset

class VideoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_object(self):
        obj = super().get_object()
        user = self.request.user

        # Allow access if admin/staff
        if user.is_staff or user.role in ['admin', 'staff']:
            return obj

        # Allow access if student is enrolled in the course
        if user.role == 'student':
            is_enrolled = Enrollment.objects.filter(user=user, course=obj.course).exists()
            if is_enrolled:
                return obj
            else:
                raise PermissionDenied("You are not enrolled in this course.")

        raise PermissionDenied("You do not have permission to access this video.")

class CourseSyllabusWithVideosView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        user = request.user

        # Allow admin/staff by default
        if user.is_staff or user.role in ['admin', 'staff']:
            pass
        else:
            from course.models import Course  # Avoid circular import
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                return Response({"detail": "Course not found."}, status=404)

            if not is_user_enrolled(user, course):
                raise PermissionDenied("You are not enrolled in this course.")

        syllabus = Syllabus.objects.filter(course_id=course_id).prefetch_related('videos')
        serializer = SyllabusWithVideosSerializer(syllabus, many=True)
        return Response(serializer.data)

class SyllabusContentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        syllabus = Syllabus.objects.filter(course_id=course_id)
        serializer = SyllabusWithContentSerializer(syllabus, many=True)
        return Response(serializer.data)

# Previous/Current/Next video navigation API.
class VideoNavigationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id, video_id):
        course = get_object_or_404(Course, id=course_id)
        videos = Video.objects.filter(course=course).order_by('syllabus__order')
        current_video = get_object_or_404(Video, id=video_id)

        video_list = list(videos)
        try:
            current_index = video_list.index(current_video)
        except ValueError:
            return Response({"detail": "Video not found in course."}, status=404)

        previous_video = video_list[current_index - 1] if current_index > 0 else None
        next_video = video_list[current_index + 1] if current_index < len(video_list) - 1 else None

        return Response({
            "previous_video": VideoMiniSerializer(previous_video).data if previous_video else None,
            "current_video": VideoMiniSerializer(current_video).data,
            "next_video": VideoMiniSerializer(next_video).data if next_video else None,
        })