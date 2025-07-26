from rest_framework import generics
from .models import LiveSession, Video
from .serializers import LiveSessionSerializer, VideoSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsStaffOrReadOnly

# LiveSession Views (with batch filtering + permission)
class LiveSessionListCreateView(generics.ListCreateAPIView):
    serializer_class = LiveSessionSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        queryset = LiveSession.objects.all()
        batch_id = self.request.query_params.get('batch')
        if batch_id:
            queryset = queryset.filter(batch_id=batch_id)
        return queryset

class LiveSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = LiveSession.objects.all()
    serializer_class = LiveSessionSerializer
    permission_classes = [IsStaffOrReadOnly]

# Video Views (with course filtering + permission)
class VideoListCreateView(generics.ListCreateAPIView):
    serializer_class = VideoSerializer
    permission_classes = [IsStaffOrReadOnly]

    def get_queryset(self):
        queryset = Video.objects.all()
        course_id = self.request.query_params.get('course')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset

class VideoDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [IsStaffOrReadOnly]