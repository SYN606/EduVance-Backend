from django.urls import path
from .views import UserCreateView, UserLoginView, SendOTPView, OTPVerifyView, OTPLoginVerifyView, TokenRefreshView

urlpatterns = [
    path('api/register/', UserCreateView.as_view(), name='user-register'),
    path('api/login/', UserLoginView.as_view(), name='user-login'),
    path('api/request-otp/', SendOTPView.as_view(), name='request-otp'),
    path('api/verify-otp/', OTPLoginVerifyView.as_view(), name='verify-otp'),
    path('api/token/refresh/',
         TokenRefreshView.as_view(),
         name='token-refresh'),  # For refreshing the token
]
