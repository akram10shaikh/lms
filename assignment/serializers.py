from rest_framework import serializers
from .models import Assignment, AssignmentSubmission

# 🔹 Assignment Serializer
class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = "__all__"
        read_only_fields = ["created_by", "created_at"]

# 🔹 Submission Serializer (used when student submits)
class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssignmentSubmission
        fields = ["id", "assignment", "submitted_file", "submitted_text"]

# 🔹 Submission List Serializer (used for viewing submissions / grading)
class AssignmentSubmissionListSerializer(serializers.ModelSerializer):
    student = serializers.StringRelatedField(read_only=True)
    assignment = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = AssignmentSubmission
        fields = ["id", "assignment", "student", "submitted_file", "submitted_text", "grade", "submitted_at"]
