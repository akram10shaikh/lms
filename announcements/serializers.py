from rest_framework import serializers
from .models import Announcement

class AnnouncementSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.get_full_name", read_only=True)
    sender_email = serializers.EmailField(source="sender.email", read_only=True)
    batch_name = serializers.CharField(source="batch.batch_name", read_only=True)   # assuming Batch has `name`
    course_name = serializers.CharField(source="course.title", read_only=True) # assuming Course has `title`

    class Meta:
        model = Announcement
        fields = [
            "id",
            "title",
            "message",
            "created_at",
            "sender",
            "sender_name",
            "sender_email",
            "batch",
            "batch_name",
            "course",
            "course_name",
        ]
