from django.db import models
from django.utils import timezone
from datetime import timedelta


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
