from django.db import models
from django.conf import settings
from course.models import Course

class Batch(models.Model):
    batch_name = models.CharField(max_length=100)
    batch_specific_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='batches')
    mentors_assigned = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        limit_choices_to={'role': 'staff'}
    )

    # New Staff Roles
    course_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='course_managed_batches',
        limit_choices_to={'role': 'staff'}
    )
    content_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='content_managed_batches',
        limit_choices_to={'role': 'staff'}
    )
    batch_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='batch_managed_batches',
        limit_choices_to={'role': 'staff'}
    )
    announcement_manager = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='announcement_managed_batches',
        limit_choices_to={'role': 'staff'}
    )

    # Dates
    start_date = models.DateField()
    end_date = models.DateField()

    # Archival flag
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.batch_name


class BatchStudent(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='students')
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'}
    )

    def __str__(self):
        return f"{self.student.email} - {self.batch.batch_name}"
