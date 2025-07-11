from django.urls import path
from .views import (
<<<<<<< HEAD
    ReviewListCreateView, ReviewDetailView,
    CategoryListCreateAPIView, CategoryDetailAPIView,
    FAQListCreateView, FAQDetailView,
)

urlpatterns = [
    # Categories
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),

    # Reviews
=======
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
>>>>>>> 8f3ee436e60f4f15c3289a8809e3b814e1e0414a
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),

    # FAQs
    path('faqs/', FAQListCreateView.as_view(), name='faq-list-create'),
    path('faqs/<int:pk>/', FAQDetailView.as_view(), name='faq-detail'),
]
