from django.contrib import admin
from .models import Assignment, AssignmentSubmission

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "due_date", "created_by", "created_at")
    search_fields = ("title", "course__title", "created_by__email")
    list_filter = ("course", "due_date", "created_at")

@admin.register(AssignmentSubmission)
class AssignmentSubmissionAdmin(admin.ModelAdmin):
    list_display = ("assignment", "student", "submitted_at", "grade")
    search_fields = ("assignment__title", "student__email")
    list_filter = ("submitted_at", "grade")
    readonly_fields = ("submitted_at",)
