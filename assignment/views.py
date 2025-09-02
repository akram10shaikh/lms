from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import Assignment, AssignmentSubmission
from .serializers import (
    AssignmentSerializer,
    AssignmentSubmissionSerializer,
    AssignmentSubmissionListSerializer,
)
from course.models import Course, Enrollment


# 🔹 Permission check for Admin only
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "admin"


# ---------------- Assignment Views ---------------- #

class AssignmentCreateView(generics.CreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAdmin]   # ✅ Only admin can create

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class AssignmentListView(generics.ListAPIView):
    serializer_class = AssignmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.role == "admin":
            return Assignment.objects.all()
        elif user.role == "student":
            # student should only see assignments for courses they enrolled in
            enrolled_courses = Enrollment.objects.filter(student=user).values_list("course_id", flat=True)
            return Assignment.objects.filter(module__course_id__in=enrolled_courses)
        return Assignment.objects.none()


class AssignmentUpdateView(generics.UpdateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAdmin]  # ✅ Only admin can update


class AssignmentDeleteView(generics.DestroyAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [IsAdmin]  # ✅ Only admin can delete


# ---------------- Assignment Submission Views ---------------- #

class SubmitAssignmentView(generics.CreateAPIView):
    serializer_class = AssignmentSubmissionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        user = self.request.user
        assignment = serializer.validated_data["assignment"]

        # check student is enrolled in course
        if not Enrollment.objects.filter(student=user, course=assignment.course).exists():
            raise PermissionError("You are not enrolled in this course")

        serializer.save(student=user)


class MySubmissionsView(generics.ListAPIView):
    serializer_class = AssignmentSubmissionListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return AssignmentSubmission.objects.filter(student=self.request.user)


class GradeAssignmentView(generics.UpdateAPIView):
    queryset = AssignmentSubmission.objects.all()
    serializer_class = AssignmentSubmissionSerializer  # ✅ use correct serializer
    permission_classes = [IsAdmin]  # Only admin can grade

    def update(self, request, *args, **kwargs):
        submission = self.get_object()
        grade = request.data.get("grade")
        if not grade:
            return Response({"error": "Grade is required"}, status=status.HTTP_400_BAD_REQUEST)

        submission.grade = grade
        submission.save()
        return Response({
            "message": "Grade assigned successfully",
            "student": submission.student.email,
            "assignment": submission.assignment.title,
            "grade": submission.grade
        })
