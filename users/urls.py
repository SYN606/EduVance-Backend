from django.urls import path
from .views import (UserLoginView, OTPVerifyView, SendOTPView,
                    TokenRefreshView, StudentProfileView, UserLogoutView)

urlpatterns = [
    path('api/login/', UserLoginView.as_view(), name='user-login'),
    path('api/verify-otp/', OTPVerifyView.as_view(), name='verify-otp'),
    path('api/request-otp/', SendOTPView.as_view(), name='request-otp'),
    path('api/token/refresh/',
         TokenRefreshView.as_view(),
         name='token-refresh'),
    path('api/student/profile/',
         StudentProfileView.as_view(),
         name='student-profile'),
    path('api/logout/', UserLogoutView.as_view(),
         name='user-logout'),  # Logout endpoint
]
