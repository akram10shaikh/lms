import uuid

from django.db import models
from django.conf import settings
from course.models import Course

class Batch(models.Model):
    batch_name = models.CharField(max_length=100)
    batch_code = models.CharField(max_length=100, unique=True)
    batch_specific_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='batches')
    staff = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='staff_batches')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.batch_name} - {self.batch_specific_course.title}"

class BatchStudent(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='batch_students')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_suspended = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.student} in {self.batch}"

class BatchStaff(models.Model):
    batch = models.ForeignKey(Batch, related_name="batch_staff", on_delete=models.CASCADE)
    staff = models.ForeignKey(settings.AUTH_USER_MODEL, limit_choices_to={'is_staff': True}, on_delete=models.CASCADE)
    added_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('batch', 'staff')  # Prevent duplicate staff

    def __str__(self):
        return f"{self.staff} in {self.batch}"