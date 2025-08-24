from rest_framework import permissions

class CanManageAnnouncements(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        # Admins always allowed
        if user.is_superuser:
            return True
        # Staff with announcement access
        return hasattr(user, "staffprofile") and user.staffprofile.has_announcement_management_access


class CanSendLimitedAnnouncements(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        return (
            hasattr(user, "staffprofile")
            and user.staffprofile.has_content_management_access
        )
