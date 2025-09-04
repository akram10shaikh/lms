from datetime import timedelta
from decimal import Decimal
from django.db import models
from django.conf import settings  # For linking to your custom User model
from django.utils import timezone




# Create your models here.
#Categories (Areas of Interest)
class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    icon = models.ImageField(upload_to='categories/icons/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

#author
class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='authors/images/', blank=True, null=True)
    organization = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

#Courses
class Course(models.Model):
    BADGE_CHOICES=[
        ('top_author','Top Author'),
        ('editors_choice',"Editor's Choice"),
        ('best_seller','Best Seller'),
        ("none",'None'),
    ]

    category = models.ForeignKey(Category,related_name='courses',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)

    short_description = models.CharField(max_length=255, null=True)
    long_description = models.TextField(null=True, blank=True)

    assignment_count = models.PositiveIntegerField(default=0)
    certificate_of_achievement = models.BooleanField(default=True)
    lifetime_access = models.BooleanField(default=True)
    live_record_session = models.BooleanField(default=True)

    author = models.ForeignKey(Author, related_name='courses', on_delete=models.CASCADE)
    duration = models.CharField(max_length=50)
    thumbnail = models.ImageField(upload_to='courses/thumbnails/',blank=True)


    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discounted_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discounted_percentage = models.PositiveIntegerField(null=True, blank=True)
    discount_end_date = models.DateTimeField(null=True, blank=True)

    average_rating = models.FloatField(default=0.0)
    review_count = models.PositiveIntegerField(default=0)

    is_archived = models.BooleanField(default=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_trending = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)

    special_tag=models.CharField(
        max_length=20,
        choices=BADGE_CHOICES,
        default='none',
        help_text="Special tag for the course (e.g., Top Author, Editor\'s Choice)"
    )

    def update_rating_stats(self):
        reviews = self.reviews.all()
        self.review_count = reviews.count()
        self.average_rating = reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0
        self.save()

    def is_discount_active(self):
        return self.discount_end_date and timezone.now() < self.discount_end_date

    def get_time_left_for_discount(self):
        if self.discount_end_date and timezone.now() < self.discount_end_date:
            return self.discount_end_date - timezone.now()
        return timedelta(0)

    def get_discount_days_left_text(self):
        if self.discount_end_date and timezone.now() < self.discount_end_date:
            days_left = (self.discount_end_date.date() - timezone.now().date()).days

            if days_left == 1:
                return "1 day left"
            elif days_left > 1:
                return f"{days_left} days left"
            return "Offer Expired"

    def save(self, *args, **kwargs):
        if self.discounted_percentage and self.original_price:
            self.discounted_price = self.original_price * (1 - Decimal(self.discounted_percentage) / Decimal(100))
        super().save(*args, **kwargs)  # Always save

    def __str__(self):
        return self.title

#What You’ll Learn
class LearningPoint(models.Model):
    course = models.ForeignKey(Course, related_name='learning_points', on_delete=models.CASCADE)
    point = models.CharField(max_length=300)

    def __str__(self):
        return f"{self.course.title} - {self.point}"

#Course Inclusions
class CourseInclusion(models.Model):
    course = models.ForeignKey(Course, related_name='inclusions', on_delete=models.CASCADE)
    item = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.course.title} - {self.item}"

#course materials
class CourseSection(models.Model):
    course = models.ForeignKey(Course, related_name='sections', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    file=models.FileField(upload_to='course_materials/',blank=True,null=True)

    def __str__(self):
        return f"{self.course.title} - {self.title}"

#Reviews
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='reviews',on_delete=models.CASCADE)
    course = models.ForeignKey(Course,related_name='reviews',on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.course} ({self.rating})"

#FAQ
class FAQ(models.Model):

    question = models.CharField(max_length=300)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question

#course enrollment
class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='enrollments', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    progress_percent = models.FloatField(default=0.0)       #Used to show completion status on My Learnings page
    last_watched_video = models.ForeignKey('content.Video', on_delete=models.SET_NULL, null=True, blank=True)     #Used to resume where left off

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user} enrolled in {self.course}"


