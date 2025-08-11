from django.shortcuts import get_object_or_404
from rest_framework import serializers

from content.models import Module
from content.modules import ModuleMiniSerializer
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

    module = ModuleMiniSerializer(read_only=True)
    module_id = serializers.PrimaryKeyRelatedField(
        queryset=Module.objects.all(),
        source='module',
        write_only=True
    )

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'duration', 'total_marks', 'is_active', 'questions']


class QuizListSerializer(serializers.ModelSerializer):
    module = ModuleMiniSerializer(read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'duration', 'total_marks', 'is_active']


class QuizAnswerSerializer(serializers.Serializer):
    question = serializers.IntegerField()
    selected_option = serializers.IntegerField()

class SubmitQuizSerializer(serializers.Serializer):
    quiz_id = serializers.IntegerField()
    answers = QuizAnswerSerializer(many=True)

    def validate(self, data):
        quiz = get_object_or_404(Quiz, pk=data['quiz_id'], is_active=True)
        data['quiz'] = quiz
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        quiz = validated_data['quiz']
        answers_data = validated_data['answers']
        score = 0

        attempt = QuizAttempt.objects.create(student=user, quiz=quiz)

        for ans in answers_data:
            question = get_object_or_404(QuizQuestion, id=ans['question'], quiz=quiz)
            selected_option = get_object_or_404(QuizOption, id=ans['selected_option'], question=question)

            is_correct = selected_option.is_correct
            if is_correct:
                score += question.mark

            QuizAnswer.objects.create(
                attempt=attempt,
                question=question,
                selected_option=selected_option,
                is_correct=is_correct
            )

        attempt.score = score
        attempt.save()
        return attempt

class QuizAttemptSerializer(serializers.ModelSerializer):
    quiz = QuizListSerializer()

    class Meta:
        model = QuizAttempt
        fields = ['id', 'quiz', 'score', 'attempted_on']