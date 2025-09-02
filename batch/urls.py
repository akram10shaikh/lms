from django.urls import path
from .views import (
    BatchListCreateView,
    BatchDetailView,
    BatchStudentListCreateView,
    BatchStudentDetailView,
    SuspendedBatchStudentListView,
    BatchStaffAssignView,
    SuspendStudentView, SuspendedStudentsInBatchView, BatchStaffListCreateView, BatchStaffDetailView,
    ArchivedBatchListView, ActiveBatchListView,
)

urlpatterns = [
    path('batches/', BatchListCreateView.as_view(), name='batch-list-create'),
    path('batches/<int:pk>/', BatchDetailView.as_view(), name='batch-detail'),
    path('batch-students/', BatchStudentListCreateView.as_view(), name='batchstudent-list-create'),
    path('batch-students/<int:pk>/', BatchStudentDetailView.as_view(), name='batchstudent-detail'),
    path('batch-students/<int:pk>/suspend/', SuspendStudentView.as_view(), name='suspend-student'),
    path('batch-suspended-students/', SuspendedBatchStudentListView.as_view(), name='suspended-students'),
    path('batch/<int:batch_id>/suspended-students/', SuspendedStudentsInBatchView.as_view(), name='suspended-students-in-batch'),
    path('batches/<int:batch_id>/assign-staff/', BatchStaffAssignView.as_view(), name='batch-assign-staff'),
    path("batch-staff/", BatchStaffListCreateView.as_view(), name="batchstaff-list-create"),
    path("batch-staff/<int:pk>/", BatchStaffDetailView.as_view(), name="batchstaff-detail"),
    path('archived-batches/', ArchivedBatchListView.as_view(), name='archived-batch-list'),
    path('active-batches/', ActiveBatchListView.as_view(), name='active-batches'),
]

