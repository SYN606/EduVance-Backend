from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.conf import settings
from .models import OTP, StudentProfile
from .serializers import LoginSerializer, OTPVerifySerializer, StudentProfileSerializer
from .otp import send_otp_email


# Helper function to set JWT cookies in the response
def set_jwt_cookie(response, access_token, refresh_token):
    response.set_cookie('access_token',
                        access_token,
                        httponly=True,
                        secure=settings.SECURE_SSL_REDIRECT,
                        samesite='Strict',
                        max_age=3600)

    response.set_cookie('refresh_token',
                        refresh_token,
                        httponly=True,
                        secure=settings.SECURE_SSL_REDIRECT,
                        samesite='Strict',
                        max_age=3600 * 24 * 30)

    return response


# Helper function to clear JWT cookies in the response
def clear_jwt_cookie(response):
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response


# User Login View
class UserLoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']

            # Check if user is already OTP verified
            if user.verified:
                # Generate JWT tokens directly if already verified
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token

                response = Response(
                    {
                        'message': 'Login successful.',
                        'access_token': str(access_token),
                        'refresh_token': str(refresh)
                    },
                    status=status.HTTP_200_OK)

                # Set JWT tokens in cookies
                response = set_jwt_cookie(response, str(access_token),
                                          str(refresh))

                return response

            # If the user is not OTP verified, send OTP to email
            otp_instance = send_otp_email(user)

            # Generate JWT tokens for OTP verification step
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            response = Response(
                {
                    'message':
                    'Login successful. OTP has been sent to your email.',
                    'otp_expiration': otp_instance.expired_at.isoformat(),
                    'user_id': user.id
                },
                status=status.HTTP_200_OK)

            # Set JWT tokens in cookies
            response = set_jwt_cookie(response, str(access_token),
                                      str(refresh))

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# OTP Verification View (for users who need to verify OTP)
class OTPVerifyView(APIView):

    def post(self, request):
        user_id = request.data.get('user_id')
        otp_code = request.data.get('otp')

        try:
            user = User.objects.get(id=user_id)

            # Check if the user is already OTP verified
            if user.verified:
                return Response({'message': 'User already verified!'},
                                status=status.HTTP_200_OK)

            # Verify OTP only for non-verified users
            otp_instance = OTP.objects.filter(
                user=user, otp=otp_code).latest('created_at')

            if otp_instance.is_expired():
                return Response({'error': 'OTP has expired'},
                                status=status.HTTP_400_BAD_REQUEST)

            # Mark user as verified
            user.verified = True
            user.save()

            # Generate JWT tokens after OTP verification
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            response = Response(
                {
                    'message': 'OTP verified successfully. Login complete.',
                    'access_token': str(access_token),
                    'refresh_token': str(refresh)
                },
                status=status.HTTP_200_OK)

            # Set JWT tokens in cookies
            response = set_jwt_cookie(response, str(access_token),
                                      str(refresh))

            return response

        except User.DoesNotExist:
            return Response({'error': 'Invalid user ID'},
                            status=status.HTTP_400_BAD_REQUEST)
        except OTP.DoesNotExist:
            return Response({'error': 'Invalid OTP'},
                            status=status.HTTP_400_BAD_REQUEST)


# Send OTP View (for logged-in users)
class SendOTPView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        otp_instance = send_otp_email(user)

        return Response(
            {
                'message': 'OTP sent to your email.',
                'otp_expiration': otp_instance.expired_at.isoformat()
            },
            status=status.HTTP_200_OK)


# Token Refresh View
class TokenRefreshView(APIView):
    permission_classes = []  # Allow anyone to refresh the token

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({'error': 'Refresh token missing'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token

            return Response({'access_token': str(access_token)},
                            status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'error': 'Invalid or expired refresh token'},
                            status=status.HTTP_400_BAD_REQUEST)


# Student Profile View (Retrieve and Update Student Profile)
class StudentProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            student_profile = StudentProfile.objects.get(user=request.user)
            serializer = StudentProfileSerializer(student_profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except StudentProfile.DoesNotExist:
            return Response({'error': 'Student profile not found'},
                            status=status.HTTP_404_NOT_FOUND)

    def put(self, request):
        try:
            student_profile = StudentProfile.objects.get(user=request.user)
            serializer = StudentProfileSerializer(student_profile,
                                                  data=request.data,
                                                  partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
        except StudentProfile.DoesNotExist:
            return Response({'error': 'Student profile not found'},
                            status=status.HTTP_404_NOT_FOUND)


# User Logout View
class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Invalidate the refresh token
        refresh_token = request.COOKIES.get('refresh_token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklist the token
            except Exception:
                pass

        # Clear the cookies
        response = Response({'message': 'Logout successful'},
                            status=status.HTTP_200_OK)
        response = clear_jwt_cookie(response)

        return response
