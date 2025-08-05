from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from accounts.permissions import IsAdmin, IsStaff
from content.models import Video
from .models import Category, Course, Review, FAQ, Enrollment, Author
from .permissions import canArchiveCourse, canDeleteCourse, IsCourseManager
from .serializers import (
    CategorySerializer,
    CourseDetailSerializer,
    CourseFilterSerializer,
    ReviewSerializer,
    CreateReviewSerializer,
    FAQSerializer,
    CourseListSerializer,
    CreateFAQSerializer, EnrollmentSerializer, AuthorSerializer, EnrollmentProgressUpdateSerializer,)

User = get_user_model()

# ---------------- CATEGORY VIEWS ----------------

class CategoryListCreateAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        categories = Category.objects.all()
        data = []
        for category in categories:
            serializer = CategorySerializer(category)
            category_data = serializer.data
            category_data['course_count'] = category.courses.count()
            data.append(category_data)
        return Response(data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category)
        data = serializer.data
        data['course_count'] = category.courses.count()
        return Response(data)

    def put(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        category = Category.objects.get(pk=pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
        except Category.DoesNotExist:
            return Response({'error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TopNewCourseListAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        thirty_days_ago = timezone.now() - timedelta(days=30)
        courses = Course.objects.annotate(avg_rating=Avg('reviews__rating')).filter(
            created_at__gte=thirty_days_ago, avg_rating__gte=4
        ).order_by('-avg_rating')

        serializer = CourseFilterSerializer(courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TopNewCourseDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return None

    def get(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseDetailSerializer(course)
        return Response(serializer.data)

    def put(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseDetailSerializer(course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CourseDetailSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response({'error': 'Course not found'}, status=status.HTTP_404_NOT_FOUND)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ---------------- TRENDING COURSES ----------------

class TrendingCourseAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        trending_courses = Course.objects.filter(is_trending=True).annotate(
            avg_rating=Avg('reviews__rating')).order_by('-avg_rating')
        serializer = CourseFilterSerializer(trending_courses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class TrendingCourseDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk, is_trending=True)
        except Course.DoesNotExist:
            return None

    def get(self, request, pk):
        course = self.get_object(pk)
        if not course:
            return Response({'error': 'Trending course not found'}, status=status.HTTP_404_NOT_FOUND)
        #serializer = CourseDetailSerializer(course)
        serializer = CourseDetailSerializer(course, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

# ---------------- REVIEW VIEWS ----------------

class ReviewListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Review.objects.all()
        course_id = self.request.query_params.get('course_id')
        if course_id:
            queryset = queryset.filter(course_id=course_id)
        return queryset

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateReviewSerializer
        return ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if serializer.instance.user != self.request.user:
            raise PermissionDenied("You can only update your own reviews")
        serializer.save()

    def perform_destroy(self, instance):
        if instance.user != self.request.user:
            raise PermissionDenied("You can only delete your own reviews")
        instance.delete()

# ---------------- FAQ VIEWS ----------------

class FAQListCreateView(generics.ListCreateAPIView):
    queryset = FAQ.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = FAQSerializer
    permission_classes = [permissions.AllowAny]

class FAQDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [permissions.IsAdminUser]

# ---------------- COURSE VIEWS ----------------

class CourseListCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        courses = Course.objects.filter(is_archived=False)
        serializer = CourseListSerializer(courses, many=True, context={'request': request})
        return Response(serializer.data, status=200)

    def post(self, request):
        if not IsCourseManager().has_permission(request, self):
            return Response({'error': 'You do not have permission to create courses.'}, status=403)

        serializer = CourseDetailSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            course = serializer.save(created_by=request.user)
            return Response(CourseDetailSerializer(course, context={'request': request}).data, status=201)
        return Response(serializer.errors, status=400)

class CourseDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Course, pk=pk)

    def get(self, request, pk):
        course = self.get_object(pk)
        serializer = CourseDetailSerializer(course, context={'request': request})
        return Response(serializer.data)

    def put(self, request, pk):
        course = self.get_object(pk)
        if not IsCourseManager().has_permission(request, self):
            return Response({'error': 'You do not have permission to edit courses.'}, status=403)

        serializer = CourseDetailSerializer(course, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def patch(self, request, pk):
        course = self.get_object(pk)
        if not IsCourseManager().has_permission(request, self):
            return Response({'error': 'You do not have permission to edit courses.'}, status=403)

        serializer = CourseDetailSerializer(course, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        course = self.get_object(pk)
        if not canDeleteCourse().has_object_permission(request, self, course):
            return Response({'error': 'You are not allowed to delete this course.'}, status=403)

        course.delete()
        return Response({'detail': 'Course deleted successfully'}, status=204)

# Enroll in a course
class EnrollCourseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, course_id):
        course = get_object_or_404(Course, id=course_id)
        user = request.user

        if Enrollment.objects.filter(user=user, course=course).exists():
            return Response({'detail': 'Already enrolled in this course.'}, status=status.HTTP_400_BAD_REQUEST)

        enrollment = Enrollment.objects.create(user=user, course=course)
        serializer = EnrollmentSerializer(enrollment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# List of Enrollments for the currently logged-in user ("My Learnings")
class MyEnrollmentsAPIView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Enrollment.objects.filter(user=self.request.user).select_related('course', 'last_watched_video')

# List enrolled courses for the admin and staff

class UserEnrollmentListAPIView(generics.ListAPIView):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAdmin | IsStaff]

    def get_queryset(self):
        if self.request.user.role in ['admin', 'staff']:
            return Enrollment.objects.select_related('course', 'user').all()
        raise PermissionDenied("Only staff or admin can view enrollments.")


# To update a student's progress in a course they are enrolled in.
class EnrollmentProgressUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        serializer = EnrollmentProgressUpdateSerializer(data=request.data, context={'request': request})

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({"message": "Enrollment progress updated"}, status=status.HTTP_200_OK)
# ---------------- AUTHOR VIEWS ----------------

class AuthorListCreateAPIView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]

class AuthorDetailAPIView(generics.RetrieveAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [permissions.AllowAny]


class CourseArchiveAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        course = get_object_or_404(Course, pk=pk)
        if not canArchiveCourse().has_object_permission(request, self, course):
            return Response({'error': 'You are not allowed to archive this course.'}, status=403)

        course.is_archived = True
        course.save()
        return Response({'message': 'Course archived successfully.'})
