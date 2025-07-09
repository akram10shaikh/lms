from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrReadOnly(BasePermission):
    """
    Only the owner can edit or delete. Others have read-only access.
    """
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS are GET, HEAD, OPTIONS — allow them for everyone
        if request.method in SAFE_METHODS:
            return True
        # Instance must have a `user` attribute
        return obj.user == request.user
