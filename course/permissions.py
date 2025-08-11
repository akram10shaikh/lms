from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import StaffProfile


class IsCourseManager(BasePermission):
    """
    Allow access only to staff users with course management access
    """

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        try:
            staff = user.staffprofile
            return staff.has_course_management_access
        except StaffProfile.DoesNotExist:
            return False


class IsAdminUser(BasePermission):
    """
    Allows access only to admin users
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'


class canArchiveCourse(BasePermission):
    """
    Allows archiving only if no active batches, enrollments, or staff exist for the course.
    """

    def has_object_permission(self, request, view, obj):
        if request.method != 'PATCH':
            return True
        return (
                not obj.batches.exists() and
                not obj.enrollments.exists() and
                not obj.staffs.exists()
        )


class canDeleteCourse(BasePermission):
    """
    Allows deletion only for admin users if no active batches, enrollments, or staff exist
    """

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'

    def has_object_permission(self, request, view, obj):
        if request.method != 'DELETE':
            return True
        return (
                not obj.batches.exists() and
                not obj.enrollments.exists() and
                not obj.staffs.exists()
        )

