from django.contrib import admin
from .models import Category, Course, Review, FAQ

# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name','icon')
    search_fields = ('name',)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'author',
        'category',
        'price',
        'discounted_price',
        'duration',
        'is_trending',
        'is_new',
        'created_at'
    )
    list_filter = ('category', 'is_trending', 'is_new')
    search_fields = ('title', 'author')
    ordering = ('-created_at',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'course',
        'rating',
        'created_at'
    )
    list_filter = ('rating',)
    search_fields = (
        'user__username',
        'course__title'
    )


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'question',
        'created_at'
    )
    search_fields = (
        'question',
        'user__username'
    )
    ordering = ('-created_at',)
