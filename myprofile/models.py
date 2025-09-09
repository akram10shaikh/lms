from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

User = settings.AUTH_USER_MODEL

#Contact Information
from django.conf import settings

class ContactInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="contact_info")
    github_url = models.URLField(blank=True, null=True)
    linkedin_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Contact Info of {self.user.email}"


# Work Experience
class WorkExperience(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="work_experiences")
    institution_name = models.CharField(max_length=255)
    role_title = models.CharField(max_length=100)
    start_year = models.IntegerField()
    end_year = models.IntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    is_current = models.BooleanField(default=False)

    def clean(self):
        if self.is_current and self.end_year is not None:
            raise ValidationError("End year must be empty if work experience is marked as current.")
        if not self.is_current and self.end_year is None:
            raise ValidationError("End year is required if work experience is not current.")
        if self.is_current:
            qs = WorkExperience.objects.filter(user=self.user, is_current=True).exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError("User already has a current work experience.")

    def __str__(self):
        return f"{self.user.full_name} - {self.institution_name} ({self.role_title})"

#Education
class Education(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="educations")
    institution_name = models.CharField(max_length=255)
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    start_year = models.IntegerField()
    end_year = models.IntegerField(null=True, blank=True)
    is_current = models.BooleanField(default=False)

    def clean(self):
        if self.is_current and self.end_year is not None:
            raise ValidationError("End year must be empty if education is marked as current.")
        if not self.is_current and self.end_year is None:
            raise ValidationError("End year is required if education is not current.")
        if self.is_current:
            qs = Education.objects.filter(user=self.user, is_current=True).exclude(pk=self.pk)
            if qs.exists():
                raise ValidationError("User already has a current education.")

    def __str__(self):
        return f"{self.user.full_name} - {self.institution_name} ({self.degree})"


# Badges & Achievements
class Badge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="badges")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date_awarded = models.DateField(blank=True, null=True)
    image = models.ImageField(upload_to="badges/", blank=True, null=True)

    def __str__(self):
        return f"Badge: {self.title} ({self.user.email})"


# Work Preferences
class WorkPreference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="work_preference")
    desired_role = models.CharField(max_length=255)
    industry = models.CharField(max_length=255, blank=True, null=True)
    remote_preference = models.BooleanField(default=False)

    def __str__(self):
        return f"Preference of {self.user.email}"



# Additional Info
class AdditionalInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="additional_info")
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)  # PDF only

    def __str__(self):
        return f"Additional Info of {self.user.email}"


class AdditionalLink(models.Model):
    additional_info = models.ForeignKey(AdditionalInfo, on_delete=models.CASCADE, related_name="links")
    platform = models.CharField(max_length=100)  # e.g., LinkedIn, GitHub
    url = models.URLField()

    def __str__(self):
        return f"{self.platform}: {self.url}"
