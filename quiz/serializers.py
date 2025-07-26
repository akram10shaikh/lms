from rest_framework import serializers
from .models import Quiz, QuizQuestion, QuizOption, QuizAttempt, QuizAnswer


class QuizOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizOption
        fields = ['id', 'text']


class QuizQuestionSerializer(serializers.ModelSerializer):
    options = QuizOptionSerializer(many=True, read_only=True)

    class Meta:
        model = QuizQuestion
        fields = ['id', 'text', 'mark', 'options']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'duration', 'total_marks', 'is_active', 'questions']


class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = ['id', 'title', 'duration', 'total_marks', 'is_active']


class QuizAnswerSerializer(serializers.Serializer):
    question = serializers.IntegerField()
    selected_option = serializers.IntegerField()


class SubmitQuizSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()
    answers = QuizAnswerSerializer(many=True)
