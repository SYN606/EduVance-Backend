from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta


# OTP Model to store the OTP code for the user
class OTP(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    otp = models.CharField(max_length=6)  # 6-digit OTP
    created_at = models.DateTimeField(auto_now_add=True)
    expired_at = models.DateTimeField()

    def is_expired(self):
        return timezone.now() > self.expired_at

    def save(self, *args, **kwargs):
        # Set expiration time to 5 minutes from creation
        self.expired_at = timezone.now() + timedelta(minutes=5)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"OTP for {self.user.username}"


# StudentProfile Model to hold student-specific information
class StudentProfile(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name="student_profile")  # Link to User
    registration_number = models.CharField(
        max_length=100, unique=True)  # Unique registration number
    profile_picture = models.ImageField(upload_to='student_profiles/',
                                        null=True,
                                        blank=True)  # Profile picture
    name = models.CharField(max_length=255)  # Student's full name
    email = models.EmailField(unique=True)  # Student's email
    phone_number = models.CharField(max_length=15)  # Student's phone number
    college_or_school = models.CharField(
        max_length=255)  # College or School name
    address = models.TextField()  # Student's address
    enrolled_course_duration = models.CharField(
        max_length=255)  # Duration of enrolled course
    fees_left = models.DecimalField(max_digits=10,
                                    decimal_places=2)  # Fees remaining

    def __str__(self):
        return f"{self.name} - {self.registration_number}"

    def get_verified_status(self):
        return self.user.verified  # Fetch verified status from linked User model


# Extend the User model to include the 'verified' field
User.add_to_class(
    'verified',
    models.BooleanField(default=False))  # Add a verified field to User model
