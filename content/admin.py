from django.contrib import admin
from .models import LiveSession, Video, Syllabus

@admin.register(LiveSession)
class LiveSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'batch', 'start_time', 'end_time')

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'duration')

@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')  # You can customize this
    search_fields = ('title',)
    list_filter = ('course',)