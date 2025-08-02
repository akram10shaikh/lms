from rest_framework import serializers
from .models import Review, FAQ, Category, Course, Author, Enrollment, LearningPoint, CourseInclusion, CourseSection
from django.contrib.auth import get_user_model
from django.db.models import Avg
from content.serializers import VideoMiniSerializer
from content.models import Video
from progress.utils import calculate_course_progress_percent
from batch.serializers import BatchMiniSerializer

class CourseMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ['id', 'title']

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
    last_watched_video = VideoMiniSerializer(read_only=True)
    batch = BatchMiniSerializer(read_only=True)

    class Meta:
        model = Enrollment
        fields = ['id', 'user', 'course', 'batch', 'enrolled_at', 'progress_percent', 'last_watched_video']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Dynamically calculate progress
        data['progress_percent'] = calculate_course_progress_percent(
            user=instance.user,
            course=instance.course
        )
        return data

# Updating the progress of a student enrolled in a course.
class EnrollmentProgressUpdateSerializer(serializers.Serializer):
    enrollment = serializers.IntegerField()
    progress_percent = serializers.FloatField(min_value=0, max_value=100)
    last_watched_video = serializers.IntegerField()

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        enrollment_id = attrs.get('enrollment')
        video_id = attrs.get('last_watched_video')

        try:
            enrollment = Enrollment.objects.get(id=enrollment_id, user=user)
        except Enrollment.DoesNotExist:
            raise serializers.ValidationError("Enrollment not found or unauthorized.")

        course = enrollment.course

        try:
            video = Video.objects.get(id=video_id, course=course)
        except Video.DoesNotExist:
            raise serializers.ValidationError("Video not found in the enrolled course.")

        attrs['enrollment'] = enrollment
        attrs['video'] = video
        return attrs

    def save(self, **kwargs):
        enrollment = self.validated_data['enrollment']
        video = self.validated_data['video']
        progress_percent = self.validated_data['progress_percent']

        enrollment.progress_percent = progress_percent
        enrollment.last_watched_video = video
        enrollment.save()
        return enrollment