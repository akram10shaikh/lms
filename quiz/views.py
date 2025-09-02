from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Quiz, QuizQuestion, QuizOption, QuizAttempt
from .serializers import QuizSerializer, QuizAttemptSerializer, QuizQuestionSerializer, QuizOptionSerializer
from course.models import Enrollment

# ADMIN CRUD VIEWS
class QuizListCreateView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAdminUser]

class QuizRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAdminUser]

class QuizQuestionCRUDView(generics.ListCreateAPIView):
    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializer
    permission_classes = [permissions.IsAdminUser]

class QuizQuestionDetailCRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializer
    permission_classes = [permissions.IsAdminUser]

class QuizOptionCRUDView(generics.ListCreateAPIView):
    queryset = QuizOption.objects.all()
    serializer_class = QuizOptionSerializer
    permission_classes = [permissions.IsAdminUser]

class QuizOptionDetailCRUDView(generics.RetrieveUpdateDestroyAPIView):
    queryset = QuizOption.objects.all()
    serializer_class = QuizOptionSerializer
    permission_classes = [permissions.IsAdminUser]

# STUDENT VIEWS
class StudentQuizListView(generics.ListAPIView):
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        enrolled_courses = Enrollment.objects.filter(student=user).values_list("course_id", flat=True)
        return Quiz.objects.filter(course_id__in=enrolled_courses, is_active=True)

class StudentQuizDetailView(generics.RetrieveAPIView):
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        enrolled_courses = Enrollment.objects.filter(student=user).values_list("course_id", flat=True)
        return Quiz.objects.filter(course_id__in=enrolled_courses, is_active=True)

class StudentQuizAttemptView(generics.CreateAPIView):
    serializer_class = QuizAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        quiz = serializer.validated_data["quiz"]
        user = self.request.user

        # Check enrollment
        if not Enrollment.objects.filter(student=user, course=quiz.course).exists():
            raise PermissionDenied("You are not enrolled in this course.")

        serializer.save(student=user)
