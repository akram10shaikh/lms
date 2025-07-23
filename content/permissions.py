from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsStaffOrReadOnly(BasePermission):
    """
    - SAFE_METHODS (GET, HEAD, OPTIONS): Allowed for any authenticated user.
    - POST, PUT, DELETE: Only allowed for staff or superusers.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and (request.user.is_staff or request.user.is_superuser)