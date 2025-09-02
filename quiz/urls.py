from django.urls import path
from .views import (
    QuizListCreateView, QuizRetrieveUpdateDeleteView,
    QuizQuestionCRUDView, QuizQuestionDetailCRUDView,
    QuizOptionCRUDView, QuizOptionDetailCRUDView,
    StudentQuizListView, StudentQuizDetailView, StudentQuizAttemptView
)

urlpatterns = [
    # Admin CRUD
    path("admin/quizzes/", QuizListCreateView.as_view(), name="quiz-list-create"),
    path("admin/quizzes/<int:pk>/", QuizRetrieveUpdateDeleteView.as_view(), name="quiz-detail-admin"),

    path("admin/questions/", QuizQuestionCRUDView.as_view(), name="question-list-create"),
    path("admin/questions/<int:pk>/", QuizQuestionDetailCRUDView.as_view(), name="question-detail"),

    path("admin/options/", QuizOptionCRUDView.as_view(), name="option-list-create"),
    path("admin/options/<int:pk>/", QuizOptionDetailCRUDView.as_view(), name="option-detail"),

    # Student
    path("student/quizzes/", StudentQuizListView.as_view(), name="student-quiz-list"),
    path("student/quizzes/<int:pk>/", StudentQuizDetailView.as_view(), name="student-quiz-detail"),
    path("student/quizzes/attempt/", StudentQuizAttemptView.as_view(), name="student-quiz-attempt"),
]
