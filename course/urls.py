from django.urls import path
from .views import (
    CategoryListCreateAPIView,
    CategoryDetailAPIView,
    CourseListCreateAPI,
    CourseDetailAPIView,
    TopNewCourseListAPIView,
    TopNewCourseDetailAPIView,
    TrendingCourseAPIView,
    TrendingCourseDetailAPIView,
    ReviewListCreateView,
    ReviewDetailView,
    FAQListCreateView,
    FAQDetailView,
)

urlpatterns = [
    # Categories
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),

    # Courses
    path('courses/', CourseListCreateAPI.as_view(), name='course-list-create'),
    path('courses/<int:pk>/', CourseDetailAPIView.as_view(), name='course-detail'),

    # Top New Courses
    path('top-new/', TopNewCourseListAPIView.as_view(), name='top-new-courses'),
    path('top-new/<int:pk>/', TopNewCourseDetailAPIView.as_view(), name='top-new-course-detail'),

    # Trending Courses
    path('trending/', TrendingCourseAPIView.as_view(), name='trending-courses'),
    path('trending/<int:pk>/', TrendingCourseDetailAPIView.as_view(), name='trending-course-detail'),

    # Reviews
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),

    # FAQs
    path('faqs/', FAQListCreateView.as_view(), name='faq-list-create'),
    path('faqs/<int:pk>/', FAQDetailView.as_view(), name='faq-detail'),
]