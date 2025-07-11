from django.urls import path
from .views import CategoryListCreateAPIView, CategoryDetailAPIView,CourseDetailAPIView,TopNewCourseAPIView,TopNewCourseDetailAPIView

urlpatterns = [
    path('categories/',CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/',CategoryDetailAPIView.as_view(), name='category-detail'),
    path('course/<int:pk>/',CourseDetailAPIView.as_view(),name='course-detail'),
    path('course/',CourseDetailAPIView.as_view(),name='course-detail'),
    path('top-new/',TopNewCourseAPIView.as_view(),name='top-new-courses'),
    path('top-new/<int:pk>/',TopNewCourseDetailAPIView.as_view(),name='top-new-course-detail'),
]

