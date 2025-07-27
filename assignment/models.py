from django.db import models
from django.contrib.auth import get_user_model
from course.models import Course  # if assignments are linked to courses

User = get_user_model()

class Assignment(models.Model):
    course = models.ForeignKey('course.Course', on_delete=models.CASCADE, related_name='assignment')
    title = models.CharField(max_length=255)
    description = models.TextField()
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

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

