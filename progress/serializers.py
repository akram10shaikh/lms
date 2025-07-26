from rest_framework import serializers
from .models import VideoProgress, SyllabusProgress
from content.models import Video, Syllabus

class VideoProgressSerializer(serializers.ModelSerializer):
    video_title = serializers.CharField(source='video.title', read_only=True)
    video_duration = serializers.IntegerField(source='video.duration', read_only=True)

    class Meta:
        model = VideoProgress
        fields = ['id', 'student', 'video', 'video_title', 'video_duration', 'watched_seconds', 'is_completed', 'last_watched_on']
        read_only_fields = ['student', 'video_title', 'video_duration', 'is_completed', 'last_watched_on']

class SyllabusProgressSerializer(serializers.ModelSerializer):
    syllabus_title = serializers.CharField(source='syllabus.title', read_only=True)

    class Meta:
        model = SyllabusProgress
        fields = ['id', 'student', 'syllabus', 'syllabus_title', 'is_completed', 'completed_on']
        read_only_fields = ['student', 'syllabus_title', 'completed_on']