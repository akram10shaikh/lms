from django.db import models
from course.models import Course
from batch.models import Batch

class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveIntegerField(help_text="Module order within course")

    class Meta:
        ordering = ['order']
        unique_together = ['course', 'title']

    def __str__(self):
        return f"{self.course.title} - {self.title}"


class LiveSession(models.Model):
    batch= models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='live_sessions')     #Links each live session to a specific batch of students (e.g., Batch A for Python Course).
    title= models.CharField(max_length=255)     #Name of the live session.
    description= models.TextField()
    start_time= models.DateTimeField()
    end_time= models.DateTimeField()
    meeting_link= models.URLField()
    meeting_id= models.CharField(max_length=100)
    meeting_password= models.CharField(max_length=100)
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='live_sessions', null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.batch})"

# To stores pre-recorded video content for courses
class Video(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')     #Links the video to a specific course (e.g., Python for Beginners).
    syllabus = models.ForeignKey('Syllabus', on_delete=models.CASCADE, related_name='videos', null=True, blank=True)
    title = models.CharField(max_length=255)        #Title of the video/Topic name (e.g., “Intro to Variables”).
    video_file = models.FileField(upload_to='videos/')
    duration = models.PositiveIntegerField(help_text="Duration in seconds")
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='videos', null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.course})"

# To represents the structured syllabus topics in a course
class Syllabus(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='syllabus_list')      #Links this syllabus topic to a specific course (e.g. if course: "Python", its syllabus topics: "Variables", "Functions")
    title = models.CharField(max_length=255)        #name of the syllabus topic.
    order = models.PositiveIntegerField(help_text="Ordering of this topic in the course")       #display syllabus topics in proper sequence
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='syllabi', null=True, blank=True)


    def __str__(self):
        return f"{self.course.title} - {self.title}"

    class Meta:
        ordering = ['order']
        unique_together = ['course', 'title']

