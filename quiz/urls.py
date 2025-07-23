from django.urls import path
from .views import QuizListAPIView, QuizDetailAPIView, SubmitQuizAPIView

urlpatterns = [
    path('quizzes/', QuizListAPIView.as_view(), name='quiz-list'),
    path('quizzes/<int:id>/', QuizDetailAPIView.as_view(), name='quiz-detail'),
    path('quizzes/submit/', SubmitQuizAPIView.as_view(), name='quiz-submit'),
]
