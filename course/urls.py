from django.urls import path
from .views import (
    ReviewListCreateView,
    ReviewDetailView,
    CategoryListCreateAPIView,
    CategoryDetailAPIView
)

urlpatterns = [
    # Category URLs
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryDetailAPIView.as_view(), name='category-detail'),

    # Review URLs
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    path('reviews/<int:pk>/', ReviewDetailView.as_view(), name='review-detail'),
]
