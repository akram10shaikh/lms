from django.urls import path
from .views import AssignmentListView, AssignmentSubmitView, MyAssignmentSubmissionsView

urlpatterns = [
    path('assignment/', AssignmentListView.as_view(), name='assignment-list'),
    path('assignment/submit/', AssignmentSubmitView.as_view(), name='assignment-submit'),
    path('assignments/my-submissions/', MyAssignmentSubmissionsView.as_view(), name='my-assignment-submissions'),
]
