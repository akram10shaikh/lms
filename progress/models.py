from django.db import models
from django.conf import settings
from content.models import Video, Syllabus

class VideoProgress(models.Model):
    student= models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video= models.ForeignKey(Video, on_delete=models.CASCADE)
    watched_seconds= models.PositiveIntegerField(default=0)
    is_completed= models.BooleanField(default=False)
    last_watched_on= models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['student', 'video']

    def __str__(self):
        return f"{self.student} - {self.video.title} - {self.watched_seconds}s"

class SyllabusProgress(models.Model):
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    syllabus = models.ForeignKey(Syllabus, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completed_on = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['student', 'syllabus']

    def __str__(self):
        return f"{self.student} - {self.syllabus.title} - {'Completed' if self.is_completed else 'In Progress'}"