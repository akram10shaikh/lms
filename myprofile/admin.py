# Register your models here.

from django.contrib import admin
from .models import (
    ContactInfo, WorkExperience, Education,
     Badge, WorkPreference,
    AdditionalInfo, AdditionalLink
)


@admin.register(ContactInfo)
class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ("user", "github_url", "linkedin_url")
    search_fields = ("user__email", "user__full_name")



@admin.register(WorkExperience)
class WorkExperienceAdmin(admin.ModelAdmin):
    list_display = ("user", "institution_name", "role_title", "start_year", "end_year", "is_current")
    search_fields = ("user__email", "institution_name", "role_title")
    list_filter = ("is_current", "start_year", "end_year")


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("user", "institution_name", "degree", "field_of_study", "start_year", "end_year", "is_current")
    search_fields = ("user__email", "institution_name", "degree", "field_of_study")
    list_filter = ("is_current", "start_year", "end_year")


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ("user", "title", "date_awarded")
    search_fields = ("user__email", "title", "description")
    list_filter = ("date_awarded",)


@admin.register(WorkPreference)
class WorkPreferenceAdmin(admin.ModelAdmin):
    list_display = ("user", "desired_role", "industry", "remote_preference")
    search_fields = ("user__email", "desired_role", "industry")
    list_filter = ("remote_preference",)


class AdditionalLinkInline(admin.TabularInline):
    model = AdditionalLink
    extra = 1


@admin.register(AdditionalInfo)
class AdditionalInfoAdmin(admin.ModelAdmin):
    list_display = ("user", "resume")
    search_fields = ("user__email",)
    inlines = [AdditionalLinkInline]
