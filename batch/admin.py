from django.contrib import admin, messages
from django.core.exceptions import ValidationError
from .models import Batch, BatchStudent, BatchStaff, ArchivedBatch, SuspendedBatchStudent
from accounts.models import CustomUser

class BatchStaffInline(admin.TabularInline):
    model = BatchStaff
    extra = 1  # number of empty rows to show

    # Limit choices to only users with role='staff'
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "staff":
            kwargs["queryset"] = CustomUser.objects.filter(role='staff')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

class BatchStudentInline(admin.TabularInline):
    model = BatchStudent
    extra = 1

    # Limit choices to only users with role='student'
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = CustomUser.objects.filter(role='student')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Batch)
class BatchAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'batch_name', 'batch_specific_course', 'start_date', 'end_date'
    )
    list_filter = ('is_archived', 'start_date', 'end_date')
    inlines = [BatchStaffInline, BatchStudentInline]

    def get_queryset(self, request):
        # Only show non-archived batches
        return super().get_queryset(request).filter(is_archived=False)

    def has_delete_permission(self, request, obj=None):
        # Allow permanent delete only for superusers
        return request.user.is_superuser

    def save_model(self, request, obj, form, change):
        """Show friendly error if archive fails"""
        try:
            obj.save()
        except ValidationError as e:
            self.message_user(request, e.message, level=messages.ERROR)

    def delete_model(self, request, obj):
        """Show friendly error if delete fails"""
        try:
            obj.delete()
        except ValidationError as e:
            self.message_user(request, e.message, level=messages.ERROR)

@admin.register(ArchivedBatch)
class ArchivedBatchAdmin(admin.ModelAdmin):
    list_display = ('id', 'batch_name', 'batch_specific_course', 'start_date', 'end_date')
    list_filter = ('start_date', 'end_date')

    def get_queryset(self, request):
        # Only show archived batches
        return super().get_queryset(request).filter(is_archived=True)

    def has_delete_permission(self, request, obj=None):
        # Allow permanent delete only for superusers
        return request.user.is_superuser

    def delete_model(self, request, obj):
        try:
            obj.delete()
        except ValidationError as e:
            self.message_user(request, e.message, level=messages.ERROR)

@admin.register(BatchStudent)
class BatchStudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'batch', 'student')

    def get_queryset(self, request):
        # Show only non-suspended students
        return super().get_queryset(request).filter(is_suspended=False)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = CustomUser.objects.filter(role='student')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(SuspendedBatchStudent)
class SuspendedBatchStudentAdmin(admin.ModelAdmin):
    list_display = ('id', 'batch', 'student', 'is_suspended')
    list_filter = ('batch',)

    def get_queryset(self, request):
        # Only show suspended students
        return super().get_queryset(request).filter(is_suspended=True)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "student":
            kwargs["queryset"] = CustomUser.objects.filter(role='student')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(BatchStaff)
class BatchStaffAdmin(admin.ModelAdmin):
    list_display = ('batch', 'staff', 'added_on')
    search_fields = ('batch__batch_name', 'staff__email')
