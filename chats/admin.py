from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("id", "batch", "sender", "receiver", "message", "timestamp", "is_read")
    list_filter = ("batch", "is_read", "timestamp")
    search_fields = ("message", "sender__full_name", "receiver__full_name")
