from django.contrib import admin
from .models import Batch, BatchStudent
from accounts.models import CustomUser

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'batch_name', 'batch_specific_course', 'start_date', 'end_date'
    )
    list_filter = ('is_archived', 'start_date', 'end_date')
    filter_horizontal = ('staff',)

# This method limits the queryset of staff field to only users with role='staff'
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "staff":
            kwargs["queryset"] = CustomUser.objects.filter(role='staff')
        return super().formfield_for_manytomany(db_field, request, **kwargs)

@admin.register(BatchStudent)
class BatchStudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'batch', 'student')
