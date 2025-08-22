import uuid

from django.db import models
from django.conf import settings
from course.models import Course
from django.core.exceptions import ValidationError


class Batch(models.Model):
    batch_name = models.CharField(max_length=100)
    batch_code = models.CharField(max_length=100, unique=True)
    batch_specific_course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='batches')
    staff = models.ManyToManyField(settings.AUTH_USER_MODEL, through='BatchStaff', related_name='staff_batches')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.batch_name} - {self.batch_specific_course.title}"

    def clean(self):
        # Prevent archiving if staff or students exist
        if self.is_archived:
            if self.batch_staff.exists() or self.batch_students.exists():
                raise ValidationError("Cannot archive this batch while staff or students are assigned.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Prevent deletion if staff/students exist
        if self.batch_staff.exists() or self.batch_students.exists():
            raise ValidationError("Cannot delete this batch while staff or students are assigned.")
        super().delete(*args, **kwargs)

class BatchStudent(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='batch_students')
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    is_suspended = models.BooleanField(default=False)

    class Meta:
        unique_together = ('batch', 'student')      # Prevent duplicate students

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


class ArchivedBatch(Batch):
    class Meta:
        proxy = True
        verbose_name = "Archived Batch"
        verbose_name_plural = "Archived Batches"

class SuspendedBatchStudent(BatchStudent):
    class Meta:
        proxy = True
        verbose_name = "Suspended Batch Student"
        verbose_name_plural = "Suspended Batch Students"