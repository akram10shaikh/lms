from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.db.models import Q
from .models import ChatMessage
from .serializers import ChatMessageSerializer
from .permissions import IsBatchParticipant
from batch.models import BatchStudent, BatchStaff


# List messages in a batch (only for participants)
class ChatMessageListView(generics.ListAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsBatchParticipant]

    def get_queryset(self):
        batch_id = self.kwargs["batch_id"]
        user = self.request.user

        # Check role of current user in the batch
        is_student = BatchStudent.objects.filter(batch_id=batch_id, student=user).exists()
        is_staff = BatchStaff.objects.filter(batch_id=batch_id, staff=user).exists()
        qs = ChatMessage.objects.filter(batch_id=batch_id)

        if is_student:
            # student ↔ staff only
            tutor_ids = BatchStaff.objects.filter(batch_id=batch_id).values_list("staff_id", flat=True)
            return qs.filter(
                Q(sender=user, receiver_id__in=tutor_ids) |
                Q(receiver=user, sender_id__in=tutor_ids)
            )

        elif is_staff:
            # staff ↔ student only
            student_ids = BatchStudent.objects.filter(batch_id=batch_id).values_list("student_id", flat=True)
            return qs.filter(
                Q(sender=user, receiver_id__in=student_ids) |
                Q(receiver=user, sender_id__in=student_ids)
            )

        return ChatMessage.objects.none()


#Create a new chat message
class ChatMessageCreateView(generics.CreateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsBatchParticipant]

    def perform_create(self, serializer):
        user = self.request.user
        batch = serializer.validated_data.get("batch")
        receiver = serializer.validated_data.get("receiver")

        # Check sender's role in the batch
        is_student = BatchStudent.objects.filter(batch=batch, student=user).exists()
        is_staff = BatchStaff.objects.filter(batch=batch, staff=user).exists()

        # Receiver must be valid opposite role in same batch
        valid_receiver = (
            (is_student and BatchStaff.objects.filter(batch=batch, staff=receiver).exists()) or
            (is_staff and BatchStudent.objects.filter(batch=batch, student=receiver).exists())
        )

        if not valid_receiver:
            raise ValidationError({"receiver": "Receiver must be a valid tutor/student in this batch"})

        serializer.save(sender=user)


#Mark a message as read
class MarkMessageReadView(generics.UpdateAPIView):
    serializer_class = ChatMessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsBatchParticipant]
    queryset = ChatMessage.objects.all()
    lookup_field = "pk"

    def update(self, request, *args, **kwargs):
        message = self.get_object()
        if message.receiver != request.user:
            return Response({"detail": "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
        message.is_read = True
        message.save()
        return Response(ChatMessageSerializer(message).data)
