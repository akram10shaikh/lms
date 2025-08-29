from rest_framework import permissions

class CanManageAnnouncements(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        if user.is_superuser:
            return True

        # staff profile check
        return hasattr(user, "staffprofile") and getattr(
            user.staffprofile, "has_announcement_management_access", False
        )


class CanSendLimitedAnnouncements(permissions.BasePermission):

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False

        # staff profile check
        return hasattr(user, "staffprofile") and getattr(
            user.staffprofile, "has_content_management_access", False
        )
