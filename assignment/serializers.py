from rest_framework import serializers

from content.models import Module
from .models import Assignment, AssignmentSubmission
from content.modules import ModuleMiniSerializer

class AssignmentSerializer(serializers.ModelSerializer):
    module = ModuleMiniSerializer(read_only=True)
    module_id = serializers.PrimaryKeyRelatedField(queryset=Module.objects.all(), source='module', write_only=True)
    class Meta:
        model = Assignment
        fields = '__all__'

class AssignmentMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = ['id', 'title', 'due_date']

class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentSubmission
        fields = ['id', 'assignment', 'file', 'submitted_at']
        read_only_fields = ['submitted_at']

class AssignmentSubmissionListSerializer(serializers.ModelSerializer):
    assignment = AssignmentMiniSerializer()
    class Meta:
        model = AssignmentSubmission
        fields = ['id', 'assignment', 'file', 'submitted_at']
