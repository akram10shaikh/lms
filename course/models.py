from django.db import models
from django.conf import settings  # For linking to your custom User model

# Create your models here.
#Categories (Areas of Interest)
class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    icon = models.ImageField(upload_to='categories/icons/', blank=True, null=True)

    def __str__(self):
        return self.name

#author
class Author(models.Model):
    name = models.CharField(max_length=100)
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='authors/images/', blank=True, null=True)

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
    description = models.TextField()
    author = models.ForeignKey(Author, related_name='courses', on_delete=models.CASCADE)
    duration = models.CharField(max_length=50)
    thumbnail = models.ImageField(upload_to='courses/thumbnails/',blank=True)
    old_price = models.DecimalField(max_digits=8, decimal_places=2)  # Old price
    current_price = models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)  # New price
    discount_valid_until = models.DateTimeField(null=True, blank=True)
    is_trending = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    special_tag=models.CharField(
        max_length=20,
        choices=BADGE_CHOICES,
        default='none',
        help_text="Special tag for the course (e.g., Top Author, Editor\'s Choice)"
    )

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

    def __str__(self):
        return f"{self.course.title} - {self.title}"

#Reviews
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='reviews',on_delete=models.CASCADE)
    course = models.ForeignKey(Course,related_name='reviews',on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # 1 to 5
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} - {self.course} ({self.rating})"

#FAQ
class FAQ(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='faqs',
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(Course, related_name='faqs', on_delete=models.CASCADE)  # Linked to Course
    question = models.CharField(max_length=300)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
          return f"{self.course.title} - {self.question}"

#course enrollment
class Enrollment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='enrollments', on_delete=models.CASCADE)
    course = models.ForeignKey(Course, related_name='enrollments', on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f"{self.user} enrolled in {self.course}"

