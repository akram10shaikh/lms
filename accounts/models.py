from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone
import pytz


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        extra_fields.setdefault('is_active', False)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', 'admin')

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ("student", "Student"),
        ("staff", "Staff"),
        ("admin", "Admin"),
    )

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=100, blank=True)
    phone_number=models.CharField(max_length=15, unique=True, blank=True, null=True)

    time_zone=models.CharField(
        max_length=100,
        choices=[(tz, tz) for tz in pytz.common_timezones],
        blank=True,null=True
        )
    language=models.CharField(max_length=50,blank=True,null=True,default="en")

    date_of_birth=models.DateField(null=True,blank=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="student")

    #  For email verification and access control
    is_email_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    profile_image = models.ImageField(upload_to="profile_images/", null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["full_name", "role"]

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.email} ({self.role})"

    def get_full_name(self):
        return self.full_name or self.email
    
class StaffProfile(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="staffprofile")
    has_course_management_access=models.BooleanField(default=False)
    has_batch_management_access=models.BooleanField(default=False)
    has_content_management_access=models.BooleanField(default=False)
    has_announcement_management_access=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.email} - Staff Profile"
    
class NameVerification(models.Model):
    STATUS_CHOICES=[
        ('pending','Pending'),
        ('approved','Approved'),
        ('rejected','Rejected'),
    ]

    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='name_verification')
    legal_name=models.CharField(max_length=150)
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    verified_at=models.DateTimeField(blank=True,null=True)

    def __str__(self):
        return f"{self.user.email} - {self.status}"
    
class TwoFactorAuth(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="two_factor")
    is_enabled=models.BooleanField(default=False)
    secret_key=models.CharField(max_length=50,blank=True,null=True) # for TOTP apps
    backup_code=models.CharField(max_length=50,blank=True,null=True) # optional

    def __str__(self):
        return f"{self.user.email} - 2FA {'Enabled' if self.is_enabled else 'Disabled'}"