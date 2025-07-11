from django.urls import path
from .views import (
    CategoryListCreateAPIView,
    CategoryDetailAPIView,
    CourseListCreateAPI,CourseDetailAPIView,TopNewCourseListAPIView,TopNewCourseDetailAPIView,
    ReviewListCreateView, ReviewDetailView
)


urlpatterns = [
    path('categories/',CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/',CategoryDetailAPIView.as_view(), name='category-detail'),
    path('courses/',CourseListCreateAPI.as_view(),name='course-list-create'),
    path('courses/<int:pk>/',CourseDetailAPIView.as_view(),name='course-detail'),
    path('top-new/',TopNewCourseListAPIView.as_view(),name='top-new-courses'),
    path('top-new/<int:pk>/',TopNewCourseDetailAPIView.as_view(),name='top-new-course-detail'),
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]