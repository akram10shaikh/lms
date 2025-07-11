from rest_framework import serializers
from .models import Review, Category  # Keep both models
from django.contrib.auth import get_user_model

# --- Category Serializer ---
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("Category name must be unique.")
        return value

User = get_user_model()

# --- User Serializer ---
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']  # Adjust fields as needed

# --- Review Serializer ---
class ReviewSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'course', 'rating', 'feedback', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5")
        return value

# --- Create Review Serializer ---
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
