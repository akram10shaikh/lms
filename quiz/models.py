from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
User = get_user_model()

class Quiz(models.Model):
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    duration = models.IntegerField(help_text="Duration in minutes")
    total_marks = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    batch = models.ForeignKey('batch.Batch', on_delete=models.CASCADE, related_name='quizzes')
    module = models.ForeignKey('content.Module', on_delete=models.SET_NULL, null=True, blank=True, related_name='quizzes')
    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"
    def __str__(self):
        return self.title

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    mark = models.IntegerField(default=1)

    def __str__(self):
        return self.text

class QuizOption(models.Model):
    question = models.ForeignKey(QuizQuestion, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class QuizAttempt(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    attempted_on = models.DateTimeField(auto_now_add=True)

class QuizAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, related_name='answers', on_delete=models.CASCADE)
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(QuizOption, on_delete=models.SET_NULL, null=True)
    is_correct = models.BooleanField(default=False)

