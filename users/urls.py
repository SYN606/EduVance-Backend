from django.urls import path
from .views import UserCreateView, UserLoginView, SendOTPView, OTPVerifyView

urlpatterns = [
    path('api/register/', UserCreateView.as_view(), name='user-register'),
    path('api/login/', UserLoginView.as_view(), name='user-login'),
    path('api/request-otp/', SendOTPView.as_view(), name='send-otp'),
    path('api/verify-otp/', OTPVerifyView.as_view(), name='verify-otp'),
]
