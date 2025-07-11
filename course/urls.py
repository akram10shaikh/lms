from django.urls import path
from .views import CategoryListCreateAPIView, CategoryDetailAPIView, CourseDetailAPIView, TopNewCourseAPIView, \
    TopNewCourseDetailAPIView, TrendingCourseAPIView, TrendingCourseDetailAPIView, AllCoursesAPIView

from .views import ReviewListCreateView, ReviewDetailView

from .views import CategoryListCreateAPIView, CategoryDetailAPIView

urlpatterns = [
    path('categories/',CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/',CategoryDetailAPIView.as_view(), name='category-detail'),
    path('course/<int:pk>/',CourseDetailAPIView.as_view(),name='course-detail'),
    path('course/',CourseDetailAPIView.as_view(),name='course-detail'),
    path('trending/', TrendingCourseAPIView.as_view(), name='trending-courses'),
    path('trending/<int:pk>/', TrendingCourseDetailAPIView.as_view(), name='trending-course-detail'),
    path('all/', AllCoursesAPIView.as_view(), name='all-courses'),
    path('top-new/',TopNewCourseAPIView.as_view(),name='top-new-courses'),
    path('top-new/<int:pk>/',TopNewCourseDetailAPIView.as_view(),name='top-new-course-detail'),
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]