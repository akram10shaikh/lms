from django.db import models
from django.conf import settings
from course.models import Course

class Batch(models.Model):
    batch_name = models.CharField(max_length=100)
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

    def __str__(self):
        return f"{self.student} in {self.batch}"