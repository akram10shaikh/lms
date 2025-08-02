from rest_framework import generics, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Batch, BatchStudent
from .serializers import BatchSerializer, BatchStudentSerializer

# List all batches and creating a new batch.
class BatchListCreateView(generics.ListCreateAPIView):
    queryset = Batch.objects.select_related('batch_specific_course').prefetch_related('staff').all()
    serializer_class = BatchSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

# Handling individual batch records
class BatchDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Batch.objects.select_related('batch_specific_course').prefetch_related('staff').all()
    serializer_class = BatchSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]

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
