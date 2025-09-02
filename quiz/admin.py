from django.contrib import admin
from .models import Quiz, QuizQuestion, QuizOption, QuizAttempt, QuizAnswer


class QuizOptionInline(admin.TabularInline):
    model = QuizOption
    extra = 2


class QuizQuestionAdmin(admin.ModelAdmin):
    inlines = [QuizOptionInline]


# Register models (only once each)
admin.site.register(Quiz)
admin.site.register(QuizQuestion, QuizQuestionAdmin)
admin.site.register(QuizOption)
admin.site.register(QuizAttempt)
admin.site.register(QuizAnswer)

