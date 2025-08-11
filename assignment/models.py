from django.db import models
from django.contrib.auth import get_user_model

from batch.models import Batch
from course.models import Course  # if assignments are linked to courses
from content.models import Syllabus

User = get_user_model()

class Assignment(models.Model):
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, related_name='assignment')
    batch = models.ForeignKey('batch.Batch', on_delete=models.CASCADE, related_name='assignments')
    syllabus = models.ForeignKey(Syllabus, on_delete=models.SET_NULL, null=True, blank=True, related_name='assignments')
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    module = models.ForeignKey('content.Module', on_delete=models.SET_NULL, null=True, blank=True, related_name='assignments')

    def __str__(self):
        return self.title

class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, related_name='submissions')
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='assignment/')
    grade = models.FloatField(null=True, blank=True)
    feedback = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student} - {self.assignment}"

