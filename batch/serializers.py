from rest_framework import serializers
from .models import Batch, BatchStudent, BatchStaff
from accounts.models import CustomUser
from accounts.serializers import UserMiniSerializer


class BatchMiniSerializer(serializers.ModelSerializer):
    staff = UserMiniSerializer(many=True, read_only=True)

    class Meta:
        model = Batch
        fields = ['id', 'batch_name', 'batch_code', 'start_date', 'end_date', 'staff', 'is_archived']

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
        fields = ['id', 'batch_name', 'batch_code', 'start_date', 'end_date', 'batch_specific_course', 'staff', 'staff_ids', 'is_archived']

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

    def validate_batch_code(self, value):
        """
        Ensure batch_code is unique (helpful for manual validation before DB constraint error)
        """
        qs = Batch.objects.filter(batch_code=value)
        if self.instance:
            qs = qs.exclude(id=self.instance.id)
        if qs.exists():
            raise serializers.ValidationError("This batch code is already in use.")
        return value

    def update(self, instance, validated_data):
        if instance.is_archived:
            raise serializers.ValidationError("Archived batches cannot be updated.")
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
        fields = ['id', 'batch', 'student', 'batch_detail', 'student_detail', 'is_suspended']

    def validate(self, attrs):
        if self.instance and self.instance.is_suspended:
            raise serializers.ValidationError("Suspended students cannot be modified.")
        return super().validate(attrs)

class SuspendStudentSerializer(serializers.Serializer):
    is_suspended = serializers.BooleanField()

class BatchStaffAssignSerializer(serializers.Serializer):
    staff_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True
    )

    def validate_staff_ids(self, value):
        invalid_ids = []
        for staff_id in value:
            if not CustomUser.objects.filter(id=staff_id, is_staff=True).exists():
                invalid_ids.append(staff_id)
        if invalid_ids:
            raise serializers.ValidationError(f"Invalid staff IDs: {invalid_ids}")
        return value

# Assigning/removing staff to/from batches.
class BatchStaffSerializer(serializers.ModelSerializer):
    staff_detail = UserMiniSerializer(source='staff', read_only=True)

    class Meta:
        model = BatchStaff
        fields = ['id', 'batch', 'staff', 'staff_detail', 'added_on']
        extra_kwargs = {
            'batch': {'write_only': True},
            'staff': {'write_only': True},
        }

    def validate(self, data):
        batch = data.get("batch")
        staff = data.get("staff")

        if not staff.is_staff:
            raise serializers.ValidationError("Only staff users can be added to a batch.")

        if BatchStaff.objects.filter(batch=batch, staff=staff).exists():
            raise serializers.ValidationError("This staff is already assigned to the batch.")
        return data