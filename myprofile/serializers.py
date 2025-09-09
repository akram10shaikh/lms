from rest_framework import serializers
from django.conf import settings
from accounts.models import CustomUser
from course.models import Enrollment

from .models import (
    ContactInfo, WorkExperience, Education,
    Badge, WorkPreference,
    AdditionalInfo, AdditionalLink
)

User = settings.AUTH_USER_MODEL


# User (basic profile fields)
class UserProfileSerializer(serializers.ModelSerializer):
    profile_completion = serializers.SerializerMethodField()
    courses = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "id", "email", "full_name", "phone_number", "profile_image",
            "profile_completion","courses",
        ]
        read_only_fields = ["email", "role"]

    def get_courses(self, obj):
        # Only courses that user has fully completed
        completed_enrollments = Enrollment.objects.filter(
            user=obj,
            progress_percent=100.0,
            is_active=True
        )
        course_titles = [e.course.title for e in completed_enrollments]

        return course_titles

    def get_profile_completion(self, obj):
        completion = 0
        basic_fields = [
            obj.full_name, obj.phone_number, obj.profile_image,
            obj.time_zone, obj.language, obj.date_of_birth
        ]
        if all(f not in [None, "", []] for f in basic_fields):
            completion += 40

        if hasattr(obj, "contact_info") and (
                obj.contact_info.github_url or obj.contact_info.linkedin_url
        ):
            completion += 10

        if obj.work_experiences.exists():
            completion += 15

        if obj.educations.exists():
            completion += 15

        if Enrollment.objects.filter(user=obj).exists():
            completion += 5

        if obj.badges.exists():
            completion += 5

        if hasattr(obj, "work_preference") and (
                obj.work_preference.desired_role or obj.work_preference.industry
        ):
            completion += 5

        if hasattr(obj, "additional_info") and (
                obj.additional_info.resume or obj.additional_info.links.exists()
        ):
            completion += 5

        return completion


# Contact Info
class ContactInfoSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    phone_number = serializers.CharField(source="user.phone_number", read_only=True)

    class Meta:
        model = ContactInfo
        fields = ["email", "phone_number", "github_url", "linkedin_url"]


# Work Experience
class WorkExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkExperience
        fields = "__all__"
        read_only_fields = ["user"]


# Education
class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"
        read_only_fields = ["user"]

# Badges

class BadgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Badge
        fields = "__all__"
        read_only_fields = ["user"]


# Work Preferences

class WorkPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkPreference
        fields = "__all__"
        read_only_fields = ["user"]


# Additional Info
class AdditionalLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalLink
        fields = "__all__"
        read_only_fields = ["additional_info"]


class AdditionalInfoSerializer(serializers.ModelSerializer):
    links = AdditionalLinkSerializer(many=True, read_only=True)

    class Meta:
        model = AdditionalInfo
        fields = ["resume", "links"]
        read_only_fields = ["user"]
