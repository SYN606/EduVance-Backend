import random
import string
from django.core.mail import send_mail
from django.utils import timezone
from .models import OTP
from datetime import timedelta
from django.conf import settings

# Function to generate a 6-digit OTP code
def generate_otp():
    return ''.join(random.choices(string.digits, k=6))


# Function to send OTP email to the user
def send_otp_email(user):
    otp_code = generate_otp()  # Generate the OTP code
    otp_instance = OTP.objects.create(user=user, otp=otp_code)
    
    # Setting expiration time for OTP to 5 minutes from the time it is created
    otp_instance.expired_at = timezone.now() + timedelta(minutes=5)
    otp_instance.save()  # Save the OTP instance with expiration date

    # Email content
    subject = 'Your OTP Code'
    message = f'Your OTP code is {otp_code}. It will expire in 5 minutes.'

    # Sending the email to the user
    send_mail(
        subject,
        message,
        'from@example.com',  # Replace with your email address or trusted email
        [user.email],  # Send OTP to the user's email
        fail_silently=False,
    )

    # Return the OTP instance, which contains expiration data
    return otp_instance
