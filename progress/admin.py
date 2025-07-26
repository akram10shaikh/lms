from django.contrib import admin
from .models import VideoProgress

@admin.register(VideoProgress)
class VideoProgressAdmin(admin.ModelAdmin):
    list_display = ['student', 'video', 'watched_seconds', 'is_completed', 'last_watched_on']
    search_fields = ['student__username', 'video__title']
    list_filter = ['is_completed']