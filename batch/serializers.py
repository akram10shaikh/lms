from rest_framework import serializers
from .models import Batch, BatchStudent
from accounts.models import CustomUser
from course.models import Course


# Reusable user field for staff
class StaffUserField(serializers.PrimaryKeyRelatedField):
    def get_queryset(self):
        return CustomUser.objects.filter(role='staff')


class BatchSerializer(serializers.ModelSerializer):
    # Staff roles
    course_manager = StaffUserField(required=False, allow_null=True)
    content_manager = StaffUserField(required=False, allow_null=True)
    batch_manager = StaffUserField(required=False, allow_null=True)
    announcement_manager = StaffUserField(required=False, allow_null=True)

    # For better display of course title and mentor emails
    batch_specific_course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all()
    )
    mentors_assigned = serializers.PrimaryKeyRelatedField(
        queryset=CustomUser.objects.filter(role='staff'),
        many=True,
        required=False
    )

    class Meta:
        model = Batch
        fields = '__all__'


class BatchStudentSerializer(serializers.ModelSerializer):
    # Optional: Display student email instead of just ID
    student = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.filter(role='student'))
    batch = serializers.PrimaryKeyRelatedField(queryset=Batch.objects.all())

    class Meta:
        model = BatchStudent
        fields = '__all__'
