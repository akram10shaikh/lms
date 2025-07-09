from django.db import models
# Create your models here.
from django.db import models
from django.conf import settings  # For linking to your custom User model

#Categories (Areas of Interest)
class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='categories/icons/', blank=True, null=True)

    def __str__(self):
        return self.name

#Courses
class Course(models.Model):
    category = models.ForeignKey(Category,related_name='courses',on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    author = models.CharField(max_length=100)
    duration = models.CharField(max_length=50)
    course_img = models.ImageField(upload_to='courses/thumbnails/')
    price = models.DecimalField(max_digits=8, decimal_places=2)  # Old price
    discounted_price = models.DecimalField(max_digits=8, decimal_places=2,null=True, blank=True)  # New price
    discount_valid_until = models.DateTimeField(null=True, blank=True)
    is_trending = models.BooleanField(default=False)
    is_new = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

#Reviews
class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='reviews',on_delete=models.CASCADE)
    course = models.ForeignKey(Course,related_name='reviews',on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()  # 1 to 5
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.course} ({self.rating})"

#FAQ
class FAQ(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='faqs',on_delete=models.CASCADE
    )
    question = models.CharField(max_length=300)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question
