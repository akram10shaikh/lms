
from django.db import models
from rest_framework.response import Response
from rest_framework import generics, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Batch, BatchStudent, BatchStaff
from .permissions import IsAdminOrStaff
from .serializers import BatchSerializer, BatchStudentSerializer, BatchStaffAssignSerializer, SuspendStudentSerializer, \
    BatchStaffSerializer


# List all batches and creating a new batch.
class BatchListCreateView(generics.ListCreateAPIView):
    serializer_class = BatchSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Batch.objects.select_related('batch_specific_course').prefetch_related('staff', 'batch_staff')

        # Filter based on role
        if user.is_superuser:
            # Admin - all batches
            pass
        elif user.is_staff:
            # Staff - only batches where they are assigned
            queryset = queryset.filter(staff=user)
        else:
            # Student - only batches they are enrolled in
            queryset = queryset.filter(batch_students__student=user)

        # Optional filter by course_id
        course_id = self.request.query_params.get('course_id')
        if course_id:
            queryset = queryset.filter(batch_specific_course__id=course_id)

        return queryset.distinct()

# list all active batches
class ActiveBatchListView(generics.ListAPIView):
    serializer_class = BatchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        # Base queryset: only active batches
        queryset = Batch.objects.filter(is_archived=False)

        if user.is_superuser:
            # Admin can see all active batches
            return queryset

        if user.is_staff:
            # Staff sees batches they are assigned to
            return queryset.filter(models.Q(staff=user) | models.Q(batch_staff__staff=user))

        # Students see batches they are enrolled in
        return queryset.filter(enrollments__user=user)


# Handling individual batch records
class BatchDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Batch.objects.select_related('batch_specific_course').prefetch_related('staff').all()
    serializer_class = BatchSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        # If trying to archive
        is_archived = request.data.get("is_archived")
        if str(is_archived).lower() in ["true", "1"]:
            has_active_students = BatchStudent.objects.filter(batch=instance, is_suspended=False).exists()
            has_staff = instance.staff.exists()

            if has_active_students or has_staff:
                raise PermissionDenied("Cannot archive: Active students or staff are still assigned to this batch.")

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Only admins can delete batches
        if hasattr(request.user, 'is_staff') and not request.user.is_superuser:
            raise PermissionDenied("Only admins can delete batches.")
        return super().destroy(request, *args, **kwargs)

# List and create BatchStudent entries.
class BatchStudentListCreateView(generics.ListCreateAPIView):
    queryset = BatchStudent.objects.select_related('batch', 'student')
    serializer_class = BatchStudentSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

class BatchStudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BatchStudent.objects.select_related('batch', 'student')
    serializer_class = BatchStudentSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

   # Prevent update if the student is suspended
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_suspended:
            raise PermissionDenied("This student is suspended and cannot be updated.")
        return super().update(request, *args, **kwargs)

    # Prevent deletion if the student is suspended.
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.is_suspended:
            raise PermissionDenied("This student is suspended and cannot be deleted.")
        return super().destroy(request, *args, **kwargs)

# List of suspended students
class SuspendedBatchStudentListView(generics.ListAPIView):
    queryset = BatchStudent.objects.filter(is_suspended=True)
    serializer_class = BatchStudentSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = BatchStudent.objects.filter(is_suspended=True)

        # If admin, show all suspended students
        if user.role == "admin":
            return queryset

        # If staff, show only suspended students from batches they manage
        if user.role == "staff" or user.is_staff:
            return queryset.filter(batch__batch_staff__staff=user)

        # If student, show only their own suspension record
        if user.role == "student":
            return queryset.filter(student=user)

        return BatchStudent.objects.none()

class SuspendStudentView(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAdminOrStaff]

    def patch(self, request, pk):
        """Suspend or unsuspend a student in a batch"""
        serializer = SuspendStudentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            batch_student = BatchStudent.objects.get(pk=pk)
        except BatchStudent.DoesNotExist:
            return Response({"error": "BatchStudent not found"}, status=404)

        batch_student.is_suspended = serializer.validated_data['is_suspended']
        batch_student.save()

        status_str = "suspended" if batch_student.is_suspended else "unsuspended"
        return Response({"message": f"Student has been {status_str}."})

# List of only suspended students for a given batch
class SuspendedStudentsInBatchView(generics.ListAPIView):
    serializer_class = BatchStudentSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        batch_id = self.kwargs.get('batch_id')
        return BatchStudent.objects.filter(batch__id=batch_id, is_suspended=True).select_related('student', 'batch')


class BatchStaffAssignView(APIView):
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, batch_id):
        """Assign staff to batch"""
        serializer = BatchStaffAssignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        batch = Batch.objects.get(id=batch_id)
        staff_ids = serializer.validated_data["staff_ids"]
        batch.staff.add(*staff_ids)
        return Response({"message": "Staff added successfully"})

    def delete(self, request, batch_id):
        """Remove staff from batch"""
        serializer = BatchStaffAssignSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        batch = Batch.objects.get(id=batch_id)
        staff_ids = serializer.validated_data["staff_ids"]
        batch.staff.remove(*staff_ids)
        return Response({"message": "Staff removed successfully"})


class BatchStaffListCreateView(generics.ListCreateAPIView):
    queryset = BatchStaff.objects.select_related('staff', 'batch').all()
    serializer_class = BatchStaffSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAdminOrStaff]

    def get_queryset(self):
        batch_id = self.request.query_params.get('batch')
        qs = BatchStaff.objects.select_related('staff', 'batch').all()
        if batch_id:
            qs = qs.filter(batch__id=batch_id)
        return qs

class BatchStaffDetailView(generics.RetrieveDestroyAPIView):
    queryset = BatchStaff.objects.all()
    serializer_class = BatchStaffSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAdminOrStaff]

# list all archived batches for admin/staff purposes.
class ArchivedBatchListView(generics.ListAPIView):
    serializer_class = BatchSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Batch.objects.filter(is_archived=True).select_related('batch_specific_course').prefetch_related(
            'staff')

        if user.is_superuser:
            pass    # # Admin sees everything
        elif user.is_staff:
            queryset = queryset.filter(staff=user)      # Staff sees only assigned batches
        else:
            queryset = queryset.filter(batch_students__student=user)      # Students see only their enrolled batches

        return queryset.distinct()