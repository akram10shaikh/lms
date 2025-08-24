from django.db import models
from django.conf import settings
from batch.models import Batch

User = settings.AUTH_USER_MODEL

class ChatMessage(models.Model):
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages",null=True,blank=True)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["timestamp"]

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver} in {self.batch}"
