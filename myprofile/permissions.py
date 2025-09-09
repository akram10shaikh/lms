from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role in ["staff", "admin"]:
            return True

        if hasattr(obj, "user"):
            return obj.user == request.user

        if hasattr(obj, "additional_info") and hasattr(obj.additional_info, "user"):
            return obj.additional_info.user == request.user
        return False

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


class IsStaffOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ["staff", "admin"]
