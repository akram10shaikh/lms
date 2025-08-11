from django.contrib import admin
from .models import Assignment, AssignmentSubmission


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'module', 'due_date')
    list_filter = ('module',)
    search_fields = ('title', 'module__title')


@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'student', 'submitted_at', 'grade')
    search_fields = ('assignment__title', 'student__email')