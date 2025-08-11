from django.contrib import admin
from .models import LiveSession, Video, Syllabus, Module


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    ordering = ('order',)

@admin.register(LiveSession)
class LiveSessionAdmin(admin.ModelAdmin):
    list_display = ('title', 'batch', 'module', 'start_time', 'end_time')
    list_filter = ('batch', 'module')
    autocomplete_fields = ['module']

@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'module', 'duration')
    list_filter = ('course', 'module')
    search_fields = ('title', 'course__title')
    autocomplete_fields = ['course', 'module']

@admin.register(Syllabus)
class SyllabusAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'module', 'order')
    search_fields = ('title',)
    list_filter = ('course', 'module')
    ordering = ('order',)
    autocomplete_fields = ['course', 'module']