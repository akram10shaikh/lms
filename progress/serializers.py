from django.utils import timezone
from rest_framework import serializers

from course.models import Enrollment
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
    progress_percent = serializers.SerializerMethodField()

    class Meta:
        model = SyllabusProgress
        fields = ['id', 'student', 'syllabus', 'syllabus_title', 'is_completed', 'completed_on', 'progress_percent']
        read_only_fields = ['student', 'syllabus_title', 'completed_on']

    def get_progress_percent(self, obj):
        total_videos = obj.syllabus.videos.count()
        if total_videos == 0:
            return 0
        completed_videos = obj.syllabus.videos.filter(
            videoprogress__student=obj.student,
            videoprogress__is_completed=True
        ).count()
        return int((completed_videos / total_videos) * 100)

class SyllabusProgressDetailSerializer(serializers.ModelSerializer):
    is_completed = serializers.SerializerMethodField()
    progress_percent = serializers.SerializerMethodField()

    class Meta:
        model = Syllabus
        fields = ['id', 'title', 'order', 'is_completed', 'progress_percent']

    def get_is_completed(self, syllabus):
        student = self.context['request'].user
        return SyllabusProgress.objects.filter(
            student=student,
            syllabus=syllabus,
            is_completed=True
        ).exists()

    def get_progress_percent(self, syllabus):
        student = self.context['request'].user
        total_videos = syllabus.videos.count()
        completed_videos = VideoProgress.objects.filter(
            student=student,
            video__syllabus=syllabus,
            is_completed=True
        ).count()

        return int((completed_videos / total_videos) * 100) if total_videos > 0 else 0

class VideoProgressUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoProgress
        fields = ['video', 'watched_seconds', 'is_completed']
        extra_kwargs = {
            'video': {'required': True},
            'is_completed': {'required': False},
        }

    def validate_video(self, video):
        if not Video.objects.filter(id=video.id).exists():
            raise serializers.ValidationError("Invalid video.")
        return video

    def update(self, instance, validated_data):
        # Update watched_seconds and is_completed
        instance.watched_seconds = validated_data.get('watched_seconds', instance.watched_seconds)
        instance.is_completed = validated_data.get('is_completed', instance.is_completed)
        instance.save()

        # Handle syllabus completion only if video is completed.
        if instance.is_completed:
            video = instance.video
            syllabus = getattr(video, 'syllabus', None)

            if syllabus:
                student = instance.student

                # Get all videos in this syllabus
                syllabus_videos = Video.objects.filter(syllabus=syllabus)

                # Get how many videos are completed by this student
                completed_count = VideoProgress.objects.filter(
                    student=student,
                    video__in=syllabus_videos,
                    is_completed=True
                ).count()

                # If all videos are completed, mark syllabus as completed
                if completed_count == syllabus_videos.count():
                    SyllabusProgress.objects.update_or_create(
                        student=student,
                        syllabus=syllabus,
                        defaults={
                            'is_completed': True,
                            'completed_on': timezone.now()
                        }
                    )

                    course = syllabus.course
                    # Count all syllabus in this course
                    total_syllabus = Syllabus.objects.filter(course=course).count()

                    # Count how many are completed by this student
                    completed_syllabus = SyllabusProgress.objects.filter(
                        student=student,
                        syllabus__course=course,
                        is_completed=True
                    ).count()

                    # Calculate progress percentage
                    progress_percent = int((completed_syllabus / total_syllabus) * 100) if total_syllabus > 0 else 0

                    Enrollment.objects.filter(
                        user=student,
                        course=course
                    ).update(
                        progress_percent=progress_percent,
                        last_watched_video=instance.video
                    )

        return instance