from django.urls import path
from .views import AssignmentListView, AssignmentSubmitView

urlpatterns = [
    path('assignment/', AssignmentListView.as_view(), name='assignment-list'),
    path('assignment/submit/', AssignmentSubmitView.as_view(), name='assignment-submit'),
]
