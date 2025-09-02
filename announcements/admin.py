from django.contrib import admin
from .models import Announcement

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "sender", "created_at", "batch", "course")
    search_fields = ("title", "message", "sender__username")
    list_filter = ("created_at", "batch", "course")

