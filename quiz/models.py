from django.db import models
from django.contrib.auth import get_user_model
from course.models import Course, Enrollment  # assuming you have an Enrollment model

User = get_user_model()

class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, null=True, blank=True, related_name="quizzes")
    title = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    duration = models.IntegerField(help_text="Duration in minutes")
    total_marks = models.IntegerField(default=0)
    passing_marks = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
<<<<<<< HEAD

=======
    batch = models.ForeignKey('batch.Batch', on_delete=models.CASCADE, related_name='quizzes',null=True,blank=True)
    module = models.ForeignKey('content.Module', on_delete=models.SET_NULL, null=True, blank=True, related_name='quizzes')
    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"
>>>>>>> 16218d27410f71c0edef327e1a51375a248eaf50
    def __str__(self):
        return f"{self.title} ({self.course.title})"

class QuizQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()

    def __str__(self):
        return self.text

class QuizOption(models.Model):
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text

class QuizAttempt(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)
    attempted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.quiz}"

class QuizAnswer(models.Model):
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE)
    selected_option = models.ForeignKey(QuizOption, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.attempt.student} - {self.question}"
