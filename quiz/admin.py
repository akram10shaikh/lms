# quiz/admin.py

from django.contrib import admin
from .models import Quiz, QuizQuestion, QuizOption, QuizAttempt, QuizAnswer

class QuizOptionInline(admin.TabularInline):
    model = QuizOption
    extra = 4  # Show 4 option fields by default

class QuizQuestionAdmin(admin.ModelAdmin):
    list_display = ['text', 'quiz', 'mark']
    inlines = [QuizOptionInline]  # This allows adding options directly when adding a question

admin.site.register(Quiz)
admin.site.register(QuizQuestion, QuizQuestionAdmin)
admin.site.register(QuizOption)
admin.site.register(QuizAttempt)
admin.site.register(QuizAnswer)


