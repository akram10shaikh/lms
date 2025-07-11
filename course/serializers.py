from rest_framework import serializers

from .models import  Review, FAQ
from django.contrib.auth import get_user_model

from .models import Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("Category name must be unique.")
        return value


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email']  # Adjust fields as needed


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
    
# ---------- FAQ Serializers ----------
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