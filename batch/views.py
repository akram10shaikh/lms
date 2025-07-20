from rest_framework import generics, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Batch, BatchStudent
from .serializers import BatchSerializer, BatchStudentSerializer


class BatchListCreateView(generics.ListCreateAPIView):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]  # ✅ support both
    permission_classes = [permissions.IsAuthenticated]


class BatchDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Batch.objects.all()
    serializer_class = BatchSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class BatchStudentListCreateView(generics.ListCreateAPIView):
    queryset = BatchStudent.objects.all()
    serializer_class = BatchStudentSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class BatchStudentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BatchStudent.objects.all()
    serializer_class = BatchStudentSerializer
    authentication_classes = [JWTAuthentication, SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
