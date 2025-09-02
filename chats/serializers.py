from rest_framework import serializers
from batch.models import BatchStudent, BatchStaff
from .models import ChatMessage

class ChatMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.full_name", read_only=True)
    receiver_name = serializers.CharField(source="receiver.full_name", read_only=True)

    class Meta:
        model = ChatMessage
        fields = [
            "id",
            "batch",
            "sender",
            "sender_name",
            "receiver",
            "receiver_name",
            "message",
            "timestamp",
            "is_read",
        ]
        read_only_fields = ["id", "timestamp","sender", "sender_name", "receiver_name"]

        def validate(self, data):
            """
            Ensure receiver belongs to the same batch.
            """
            batch = data.get("batch")
            receiver = data.get("receiver")

            if receiver:
                is_participant = (BatchStudent.objects.filter(batch=batch, student=receiver).exists()
                        or BatchStaff.objects.filter(batch=batch, staff=receiver).exists()
                )
                if not is_participant:
                    raise serializers.ValidationError(
                        {"receiver": "Receiver must be part of the same batch."}
                    )
            return data
