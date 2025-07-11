from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Category,Course
from .serializers import CategorySerializer,CourseDetailSerializer,CourseFilterSerializer
from django.utils import timezone
from datetime import timedelta
from django.db.models import Avg


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
        serializer = CategorySerializer(category, data=request.data, partial=True)  # 👈 partial=True!
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

class CourseDetailAPIView(APIView):
    permission_classes=[permissions.AllowAny]

    def get_object(self,pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return None
        
    def get(self,request,pk):
        course=self.get_object(pk)
        if not course:
            return Response({'error':'Course not found'},status=status.HTTP_404_NOT_FOUND)
        serializer=CourseDetailSerializer(course)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=CourseDetailSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,pk):
        course=self.get_object(pk)
        if not course:
            return Response({'error':'Course not found'},status=status.HTTP_404_NOT_FOUND)
        serializer=CourseDetailSerializer(course,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,pk):
        course=self.get_object(pk)
        if not course:
            return Response({'error':'Course not found'},status=status.HTTP_404_NOT_FOUND)
        serializer=CourseDetailSerializer(course,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        course=self.get_object(pk)
        if not course:
            return Response({'error':'Course not found'},status=status.HTTP_404_NOT_FOUND)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class TopNewCourseAPIView(APIView):
    permission_classes=[permissions.AllowAny]

    def get(self,request):
        thirty_days_ago=timezone.now()-timedelta(days=30)

        courses=Course.objects.annotate(avg_rating=Avg('reviews__rating')).filter(
            created_at__gte=thirty_days_ago,avg_rating__gte=4
        ).order_by('-avg_rating')

        serializer=CourseFilterSerializer(courses,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class TopNewCourseDetailAPIView(APIView):
    permission_classes=[permissions.AllowAny]

    def get_object(self,pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return None
        
    def get(self,request,pk):
        course=self.get_object(pk)
        if not course:
            return Response({'error':'Course not found'},status=status.HTTP_404_NOT_FOUND)
        serializer=CourseDetailSerializer(course)
        return Response(serializer.data)
    
    def post(self,request):
        serializer=CourseDetailSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def put(self,request,pk):
        course=self.get_object(pk)
        if not course:
            return Response({'error':'Course not found'},status=status.HTTP_404_NOT_FOUND)
        serializer=CourseDetailSerializer(course,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self,request,pk):
        course=self.get_object(pk)
        if not course:
            return Response({'error':'Course not found'},status=status.HTTP_404_NOT_FOUND)
        serializer=CourseDetailSerializer(course,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        course=self.get_object(pk)
        if not course:
            return Response({'error':'Course not found'},status=status.HTTP_404_NOT_FOUND)
        course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)