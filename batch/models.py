from django.db import models
from django.conf import settings
from course.models import Course

class Batch(models.Model):
    batch_name = models.CharField(max_length=100)
    batch_specific_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='batches')
    mentors_assigned = models.ManyToManyField(settings.AUTH_USER_MODEL, limit_choices_to={'role': 'staff'})
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.batch_name

class BatchStudent(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='students')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})

    def __str__(self):
        return f"{self.student.email} - {self.batch.batch_name}"
