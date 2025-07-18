from rest_framework import serializers
from .models import Review, FAQ, Category, Course
from django.contrib.auth import get_user_model
from django.db.models import Avg

User = get_user_model()

# ---------- Category ----------
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("Category name must be unique.")
        return value

# ---------- Course ----------
class CourseSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    special_tag = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_rating(self, obj):
        avg_rating = obj.reviews.aggregate(avg=Avg('rating'))['avg']
        return round(avg_rating or 0, 1)

    def get_special_tag(self, obj):
        return obj.get_special_tag_display()

class CourseFilterSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    special_tag = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'thumbnail',
            'author',
            'duration',
            'current_price',
            'old_price',
            'rating',
            'special_tag',
        ]

    def get_rating(self, obj):
        avg_rating = obj.reviews.aggregate(avg=Avg('rating'))['avg']
        return round(avg_rating or 0, 1)

    def get_special_tag(self, obj):
        return obj.get_special_tag_display()

# ---------- User ----------
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']  # Adjust if needed

# ---------- Review ----------
class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'course', 'rating', 'feedback', 'created_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['course', 'rating', 'feedback']

    def validate(self, data):
        user = self.context['request'].user
        course = data['course']
        if Review.objects.filter(user=user, course=course).exists():
            raise serializers.ValidationError("You have already reviewed this course")
        return data


# ---------- FAQ ----------
class FAQSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = FAQ
        fields = ['id', 'user', 'course', 'question', 'answer', 'created_at']
        read_only_fields = ['created_at']

class CreateFAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['course', 'question', 'answer']

    def validate(self, data):
        user = self.context['request'].user
        course = data['course']
        question = data['question']
        if FAQ.objects.filter(user=user, course=course, question__iexact=question).exists():
            raise serializers.ValidationError("You have already submitted this question for this course.")
        return data