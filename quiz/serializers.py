from rest_framework import serializers
from .models import Quiz, QuizQuestion, QuizOption, QuizAttempt, QuizAnswer

class QuizOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizOption
        fields = ["id", "text", "is_correct"]  # is_correct only visible to admin

class QuizQuestionSerializer(serializers.ModelSerializer):
    options = QuizOptionSerializer(many=True, read_only=True)

    class Meta:
        model = QuizQuestion
        fields = ["id", "text", "options"]

class QuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ["id", "course", "title", "duration", "total_marks", "passing_marks", "is_active", "questions"]

class QuizAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAnswer
        fields = ["question", "selected_option"]

class QuizAttemptSerializer(serializers.ModelSerializer):
    answers = QuizAnswerSerializer(many=True, write_only=True)

    class Meta:
        model = QuizAttempt
        fields = ["id", "quiz", "score", "completed", "answers"]
        read_only_fields = ["score", "completed"]

    def create(self, validated_data):
        answers_data = validated_data.pop("answers")
        student = self.context["request"].user
        quiz = validated_data["quiz"]

        attempt = QuizAttempt.objects.create(student=student, quiz=quiz)

        score = 0
        for answer in answers_data:
            question = answer["question"]
            option = answer["selected_option"]
            QuizAnswer.objects.create(attempt=attempt, question=question, selected_option=option)

            if option.is_correct:
                score += 1

        attempt.score = score
        attempt.completed = True
        attempt.save()
        return attempt
