from rest_framework import serializers
from .models import Review, FAQ, Category, Course, Author, Enrollment, LearningPoint, CourseInclusion, CourseSection
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

# ---------- Author ----------
class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'bio','image']

# ---------- Course ----------
# class CourseSerializer(serializers.ModelSerializer):
#     rating = serializers.SerializerMethodField()
#     category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
#     special_tag = serializers.SerializerMethodField()
#     author = AuthorSerializer(read_only=True)
#     author_id = serializers.PrimaryKeyRelatedField(
#         queryset=Author.objects.all(),
#         source='author',
#         write_only=True
#     )

#     class Meta:
#         model = Course
#         fields = '__all__'

#     def get_rating(self, obj):
#         avg_rating = obj.reviews.aggregate(avg=Avg('rating'))['avg']
#         return round(avg_rating or 0, 1)

#     def get_special_tag(self, obj):
#         return obj.get_special_tag_display()

class CourseFilterSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField()
    special_tag = serializers.SerializerMethodField()
    author = AuthorSerializer(read_only=True)

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
        fields = ['id', 'email',"full_name"]  # Adjust if needed

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

#----course specific-----
class LearningPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = LearningPoint
        fields = ['point']


class CourseInclusionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseInclusion
        fields = ['item']

class CourseSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSection
        fields = ['title', 'description']

#--course details---
class CourseDetailSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all())
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(source='author', queryset=Author.objects.all(), write_only=True)

    learning_points = LearningPointSerializer(many=True, required=True)
    inclusions = CourseInclusionSerializer(many=True, required=True)
    sections = CourseSectionSerializer(many=True, required=True)

    reviews = ReviewSerializer(many=True, read_only=True)
    faqs = FAQSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()
    review_count = serializers.SerializerMethodField()
    special_tag = serializers.SerializerMethodField()
    is_enrolled = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        learning_points_data = validated_data.pop('learning_points')
        inclusions_data = validated_data.pop('inclusions')
        sections_data = validated_data.pop('sections')

        course = Course.objects.create(**validated_data)

        # Create related items
        for point_data in learning_points_data:
            LearningPoint.objects.create(course=course, **point_data)

        for item_data in inclusions_data:
            CourseInclusion.objects.create(course=course, **item_data)

        for section_data in sections_data:
            CourseSection.objects.create(course=course, **section_data)

        return course

    def get_rating(self, obj):
        avg_rating = obj.reviews.aggregate(avg=Avg('rating'))['avg']
        return round(avg_rating or 0, 1)

    def get_review_count(self, obj):
        return obj.reviews.count()

    def get_special_tag(self, obj):
        return obj.get_special_tag_display()

    def get_is_enrolled(self, obj):
        # user = self.context['request'].user
        # if user.is_authenticated:
        #     return Enrollment.objects.filter(user=user, course=obj).exists()
        # return False
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return Enrollment.objects.filter(user=request.user, course=obj).exists()
        return False

#-----Enrollment-----
class EnrollmentSerializer(serializers.ModelSerializer):
    course = CourseFilterSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'course', 'enrolled_at']
