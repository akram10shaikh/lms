from rest_framework import serializers
from .models import Batch, BatchStudent
from accounts.models import CustomUser
from accounts.serializers import UserMiniSerializer


class BatchMiniSerializer(serializers.ModelSerializer):
    staff = UserMiniSerializer(many=True, read_only=True)

    class Meta:
        model = Batch
        fields = ['id', 'batch_name', 'start_date', 'end_date', 'staff']

# Creating a new batch and assigning staff to it.
# Updating batch info and its staff
# Showing detail info for staff and course
class BatchSerializer(serializers.ModelSerializer):
    staff = UserMiniSerializer(many=True, read_only=True)   # Used to show a list of staff details
    staff_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=CustomUser.objects.filter(role='staff'),
        write_only=True,
        source='staff'
    )
    class Meta:
        model = Batch
        fields = ['id', 'batch_name', 'start_date', 'end_date', 'batch_specific_course', 'staff', 'staff_ids']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from course.serializers import CourseMiniSerializer
        self.fields['course_detail'] = CourseMiniSerializer(
            source='batch_specific_course', read_only=True
        )
    def validate_staff_ids(self, value):
        for user in value:
            if user.role != 'staff':
                raise serializers.ValidationError(
                    f"User '{user}' does not have the role 'staff'."
                )
        return value

    def update(self, instance, validated_data):
        staff_ids = validated_data.pop('staff_ids', None)
        instance = super().update(instance, validated_data)
        if staff_ids is not None:
            instance.staff.set(staff_ids)
        return instance

    def create(self, validated_data):
        staff_ids = validated_data.pop('staff_ids', [])
        instance = super().create(validated_data)
        if staff_ids:
            instance.staff.set(staff_ids)
        return instance

# Relationship between a Batch and a Student like which students are enrolled in which batch.
class BatchStudentSerializer(serializers.ModelSerializer):
    batch_detail = BatchMiniSerializer(source='batch', read_only=True)
    student_detail = UserMiniSerializer(source='student', read_only=True)

    class Meta:
        model = BatchStudent
        fields = ['id', 'batch', 'student', 'batch_detail', 'student_detail']