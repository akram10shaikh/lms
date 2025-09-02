from rest_framework.permissions import BasePermission
from batch.models import BatchStudent, BatchStaff, Batch

class IsBatchParticipant(BasePermission):
    """
    Allow only students and staff from the batch to access messages.
    """

    def has_object_permission(self, request, view, obj):
        batch = obj.batch
        return self._is_participant(request.user, batch)

    def has_permission(self, request, view):
        batch_id = view.kwargs.get("batch_id")
        if not batch_id:
            return True
        try:
            batch = Batch.objects.get(id=batch_id)
        except Batch.DoesNotExist:
            return False
        return self._is_participant(request.user, batch)

    def _is_participant(self, user, batch):
        return (
            BatchStudent.objects.filter(batch=batch, student=user).exists()
            or BatchStaff.objects.filter(batch=batch, staff=user).exists()
        )
