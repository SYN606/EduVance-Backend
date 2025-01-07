from django.urls import path
from .views import UserCreateView, UserLoginView

urlpatterns = [
    path('api/register/', UserCreateView.as_view(), name='user-register'),
    path('api/login/', UserLoginView.as_view(), name='user-login'),
]
