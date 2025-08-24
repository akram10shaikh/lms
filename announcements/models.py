from django.db import models
from django.contrib.auth import get_user_model
from course.models import Course
from batch.models import Batch

User = get_user_model()

class Announcement(models.Model):
    title = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="sent_announcements")

    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True, blank=True, related_name="announcements")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name="announcements")

    def __str__(self):
        return f"{self.title} - {self.sender}"
