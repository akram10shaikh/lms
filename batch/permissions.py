from rest_framework import permissions

class IsAdminOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # Allow admin for all actions
        if request.user.is_superuser:
            return True

        # Staff allowed for non-delete actions only
        if request.user.is_staff and request.method != 'DELETE':
            return True

        return False