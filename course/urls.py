from django.urls import path
from .views import (
    CategoryListView,
    CourseListView,
    CourseDetailView,
    ReviewListCreateView,
    ReviewDetailView,
    FAQListCreateView
)

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('courses/', CourseListView.as_view(), name='course-list'),
    path('courses/<int:pk>/', CourseDetailView.as_view(), name='course-detail'),
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
    path('faqs/', FAQListCreateView.as_view(), name='faq-list-create'),
]
