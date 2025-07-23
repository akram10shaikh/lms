from django.db import models
from course.models import Course
from batch.models import Batch

class LiveSession(models.Model):
    batch= models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='live_sessions')
    title= models.CharField(max_length=255)
    description= models.TextField()
    start_time= models.DateTimeField()
    end_time= models.DateTimeField()
    meeting_link= models.URLField()
    meeting_id= models.CharField(max_length=100)
    meeting_password= models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title} ({self.batch})"

class Video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    title = models.CharField(max_length=255)
    video_file = models.FileField(upload_to='videos/')
    duration = models.PositiveIntegerField(help_text="Duration in seconds")

    def __str__(self):
        return f"{self.title} ({self.course})"

class Syllabus(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='syllabus_list')
    title = models.CharField(max_length=255)
    order = models.PositiveIntegerField(help_text="Ordering of this topic in the course")

    def __str__(self):
        return f"{self.course.title} - {self.title}"

    class Meta:
        ordering = ['order']
        unique_together = ['course', 'title']

