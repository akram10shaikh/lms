from rest_framework import permissions

class IsAdmin(permissions.BasePermission):
    """
    Allows access only to admin users (role = admin).
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"
