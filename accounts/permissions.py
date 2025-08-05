from rest_framework.permissions import BasePermission, SAFE_METHODS


class RolePermission(BasePermission):
    allowed_roles=[]

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in self.allowed_roles
class IsStudent(BasePermission):
    """Allows access only to authenticated users with the role 'student'."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "student"

class IsStaff(BasePermission):
    """Allows access only to authenticated users with the role 'staff'."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "staff"

class IsAdmin(BasePermission):
    """Allows access only to authenticated users with the role 'admin'."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"

class IsEmailVerified(BasePermission):
    """Allows access only if user's email is verified."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_email_verified

class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff