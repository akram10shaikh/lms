from django.urls import path
from .views import AssignmentListView, AssignmentSubmitView, MyAssignmentSubmissionsView

from .views import (
    AssignmentCreateView, AssignmentListView, AssignmentDetailView,
    AssignmentUpdateView, AssignmentDeleteView, AssignmentSubmitView,
    MyAssignmentSubmissionsView
)

urlpatterns = [
    # Assignment CRUD
    path('create/', AssignmentCreateView.as_view(), name='assignment-create'),
    path('list/', AssignmentListView.as_view(), name='assignment-list'),
    path('<int:pk>/', AssignmentDetailView.as_view(), name='assignment-detail'),
    path('<int:pk>/update/', AssignmentUpdateView.as_view(), name='assignment-update'),
    path('<int:pk>/delete/', AssignmentDeleteView.as_view(), name='assignment-delete'),

    # Assignment submissions
    path('submit/', AssignmentSubmitView.as_view(), name='assignment-submit'),
    path('my-submissions/', MyAssignmentSubmissionsView.as_view(), name='my-submissions'),

]
