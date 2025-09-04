from django.urls import path
from .views import (
    AssignmentCreateView,
    AssignmentListView,
    AssignmentUpdateView,
    AssignmentDeleteView,
    SubmitAssignmentView,
    MySubmissionsView,
    GradeAssignmentView,
)

urlpatterns = [
    # Assignment CRUD (admin only for create/update/delete)
    path("assignments/", AssignmentListView.as_view(), name="assignment-list"),
    path("assignments/create/", AssignmentCreateView.as_view(), name="assignment-create"),
    path("assignments/<int:pk>/update/", AssignmentUpdateView.as_view(), name="assignment-update"),
    path("assignments/<int:pk>/delete/", AssignmentDeleteView.as_view(), name="assignment-delete"),

    # Student submissions
    path("assignments/submit/", SubmitAssignmentView.as_view(), name="assignment-submit"),
    path("assignments/my-submissions/", MySubmissionsView.as_view(), name="my-submissions"),

    # Admin grading
    path("assignments/<int:pk>/grade/", GradeAssignmentView.as_view(), name="grade-assignment"),
]
