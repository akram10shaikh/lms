from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated , AllowAny
from .models import Quiz, QuizQuestion, QuizOption, QuizAttempt, QuizAnswer
from .serializers import QuizSerializer, QuizListSerializer, SubmitQuizSerializer, QuizAttemptSerializer
from django.shortcuts import get_object_or_404


class QuizListAPIView(generics.ListAPIView):
    serializer_class = QuizListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Optional: filter by batch
        batch_id = self.request.query_params.get('batch_id')
        if batch_id:
            return Quiz.objects.filter(batch_id=batch_id, is_active=True)
        return Quiz.objects.filter(is_active=True)


class QuizDetailAPIView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'


class SubmitQuizAPIView(generics.GenericAPIView):
    serializer_class = SubmitQuizSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        quiz_id = serializer.validated_data['quiz_id']
        answers = serializer.validated_data['answers']
        quiz = get_object_or_404(Quiz, id=quiz_id)

        attempt = QuizAttempt.objects.create(
            student=request.user,
            quiz=quiz,
        )

        total_score = 0
        for ans in answers:
            question = get_object_or_404(QuizQuestion, id=ans['question_id'], quiz=quiz)
            selected_option = get_object_or_404(QuizOption, id=ans['selected_option_id'], question=question)
            is_correct = selected_option.is_correct
            if is_correct:
                total_score += question.mark

            QuizAnswer.objects.create(
                attempt=attempt,
                question=question,
                selected_option=selected_option,
                is_correct=is_correct
            )

        attempt.score = total_score
        attempt.save()

        return Response({'message': 'Quiz submitted successfully!', 'score': total_score}, status=status.HTTP_200_OK)

class ListQuizAttemptsAPIView(generics.ListAPIView):
    serializer_class = QuizAttemptSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return QuizAttempt.objects.filter(student=self.request.user).select_related('quiz')
