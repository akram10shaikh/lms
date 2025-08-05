from django.contrib import admin
from .models import Category, Course, Review, FAQ, Author, Enrollment, CourseSection, CourseInclusion, LearningPoint
from django.db.models import Avg

# ---------- CATEGORY ----------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'icon')
    search_fields = ('name',)


# ---------- AUTHOR ----------
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


# ---------- COURSE ----------
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'title',
        'author',
        'average_rating',
        'category',
        'duration',
        'is_trending',
        'is_new',
        'created_at',
        'special_tag',
        "is_archived"
    ]
    list_filter = ('category', 'is_trending', 'is_new')
    search_fields = ('title', 'author__name')
    ordering = ('-created_at',)

    def average_rating(self, obj):
        avg = obj.reviews.aggregate(avg=Avg('rating'))['avg']
        return round(avg or 0, 1)
    average_rating.short_description = 'Avg Rating'


# ---------- REVIEW ----------
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'rating', 'created_at')
    list_filter = ('rating',)
    search_fields = ('user__email', 'course__title')
    ordering = ('-created_at',)


# ---------- FAQ ----------
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'created_at')
    search_fields = ('question', 'user__email', 'course__title')
    ordering = ('-created_at',)

## Enrollment ##
@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'enrolled_at')
    list_filter = ('enrolled_at',)
    search_fields = ('user__email', 'course__title')
    ordering = ('-enrolled_at',)


# ---------- LEARNING POINT ----------
@admin.register(LearningPoint)
class LearningPointAdmin(admin.ModelAdmin):
    list_display = ('course', 'point')
    search_fields = ('course__title', 'point')


# ---------- COURSE INCLUSION ----------
@admin.register(CourseInclusion)
class CourseInclusionAdmin(admin.ModelAdmin):
    list_display = ('course', 'item')
    search_fields = ('course__title', 'item')


# ---------- COURSE SECTION ----------
@admin.register(CourseSection)
class CourseSectionAdmin(admin.ModelAdmin):
    list_display = ('course', 'title')
    search_fields = ('course__title', 'title')