from django.urls import path
from .views import (
    BatchListCreateView,
    BatchDetailView,
    BatchStudentListCreateView,
    BatchStudentDetailView
)

urlpatterns = [
    path('batches/', BatchListCreateView.as_view(), name='batch-list-create'),
    path('batches/<int:pk>/', BatchDetailView.as_view(), name='batch-detail'),
    path('batch-students/', BatchStudentListCreateView.as_view(), name='batchstudent-list-create'),
    path('batch-students/<int:pk>/', BatchStudentDetailView.as_view(), name='batchstudent-detail'),
]
