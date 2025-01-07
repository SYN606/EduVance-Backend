from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, LoginSerializer
from .otp import send_otp_email
from .models import OTP
from django.utils import timezone
from rest_framework import serializers


# User Creation View
class UserCreateView(APIView):

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Create the user
            return Response(
                {
                    'message': 'User created successfully!',
                    'user': {
                        'username': user.username,
                        'email': user.email
                    }
                },
                status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Login View
class UserLoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Generate JWT token for the user
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            return Response(
                {
                    'message': 'Login successful',
                    'access_token': str(access_token),
                    'refresh_token': str(refresh)
                },
                status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# OTP Verification Serializer
class OTPVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)


# Send OTP View (for logged-in users)
class SendOTPView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request):
        user = request.user
        otp_instance = send_otp_email(user)  # Call the function from otp.py

        return Response(
            {
                'message': 'OTP sent to your email.',
                'otp_expiration': otp_instance.expired_at.isoformat(
                )  # Provide expiration time in ISO format
            },
            status=status.HTTP_200_OK)


# OTP Verification View (for logged-in users)
class OTPVerifyView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request):
        user = request.user
        serializer = OTPVerifySerializer(data=request.data)

        if serializer.is_valid():
            otp_code = serializer.validated_data['otp']
            try:
                # Fetch the latest OTP for the user
                otp_instance = OTP.objects.filter(
                    user=user, otp=otp_code).latest('created_at')

                if otp_instance.is_expired():
                    return Response({'error': 'OTP has expired'},
                                    status=status.HTTP_400_BAD_REQUEST)

                # OTP is valid, you can proceed with the next step (authentication, user actions, etc.)
                return Response({'message': 'OTP verified successfully'},
                                status=status.HTTP_200_OK)

            except OTP.DoesNotExist:
                return Response({'error': 'Invalid OTP'},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
