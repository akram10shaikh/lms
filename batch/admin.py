from django.contrib import admin
from .models import Batch, BatchStudent

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'batch_name', 'batch_specific_course', 'start_date', 'end_date')
    filter_horizontal = ('mentors_assigned',)

@admin.register(BatchStudent)
class BatchStudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'batch', 'student')
