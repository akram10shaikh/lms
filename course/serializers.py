from rest_framework import serializers
from .models import Category,Course
from django.db.models import Avg

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

    def validate_name(self, value):
        if Category.objects.filter(name=value).exists():
            raise serializers.ValidationError("Category name must be unique.")
        return value

class CourseDetailSerializer(serializers.ModelSerializer):
    rating=serializers.SerializerMethodField()
    category=serializers.SlugRelatedField(slug_field='name',queryset=Category.objects.all())
    special_tag=serializers.SerializerMethodField()


    class Meta:
        model=Course
        fields='__all__'

    def get_rating(self,obj):
        avg_rating=obj.reviews.aggregate(avg=Avg('rating'))['avg']
        return round(avg_rating or 0, 1)
    
    def get_special_tag(self,obj):
        return obj.get_special_tag_display()

class CourseFilterSerializer(serializers.ModelSerializer):
    thumbnail=serializers.ImageField(source='course_img')
    current_price=serializers.DecimalField(source='discounted_price',max_digits=8,decimal_places=2)
    old_price=serializers.DecimalField(source='price',max_digits=8,decimal_places=2)
    rating=serializers.SerializerMethodField()
    special_tag=serializers.SerializerMethodField()

    class Meta:
        model=Course
        fields=[
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

    def get_rating(self,obj):
        avg_rating=obj.reviews.aggregate(avg=Avg('rating'))['avg']
        return round(avg_rating or 0, 1)
    
    def get_special_tag(self,obj):
        return obj.get_special_tag_display()