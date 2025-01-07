import random
import string
from django.core.mail import send_mail
from django.utils import timezone
from .models import OTP
from django.conf import settings

def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


def send_otp_email(user):
    otp_code = generate_otp()
    otp_instance = OTP.objects.create(user=user, otp=otp_code)
    otp_instance.save()
    subject = 'Your OTP Code'
    message = f'Your OTP code is {otp_code}. It will expire in 5 minutes.'

    send_mail(
        subject,
        message,
        'from@gmail.com',  # Replace with your email address or trusted email
        # 'no-reply@yourdomain.com'  # A no-reply address from your domain for production
        [user.email],
        fail_silently=False,
    )
    # send_mail(
    #     subject,
    #     message,
    #     settings.DEFAULT_FROM_EMAIL,  # Use the default from email in settings
    #     [user.email],
    #     fail_silently=False,
    # )

    return otp_instance
