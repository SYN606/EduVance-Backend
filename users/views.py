from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.conf import settings
from .serializers import UserSerializer, LoginSerializer, OTPVerifySerializer
from .otp import send_otp_email
from .models import OTP


# Helper function to set the JWT tokens in HTTP-only cookies
def set_jwt_cookie(response, access_token, refresh_token):
    """
    This function sets both the access_token and refresh_token in HTTP-only cookies.
    """
    # Setting the Access Token in an HTTP-only cookie
    response.set_cookie(
        'access_token',
        access_token,
        httponly=True,
        secure=settings.
        SECURE_SSL_REDIRECT,  # Ensure this is True in production (i.e., HTTPS)
        samesite='Strict',
        max_age=3600  # Expires in 1 hour
    )

    # Setting the Refresh Token in an HTTP-only cookie
    response.set_cookie(
        'refresh_token',
        refresh_token,
        httponly=True,
        secure=settings.
        SECURE_SSL_REDIRECT,  # Ensure this is True in production (i.e., HTTPS)
        samesite='Strict',
        max_age=3600 * 24 * 30  # Expires in 30 days
    )

    return response


# User Registration View
class UserCreateView(APIView):

    def post(self, request):
        # Deserialize user data using the UserSerializer
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Create the user

            # Create response object
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
        # Deserialize the login data using the LoginSerializer
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            # Get the authenticated user
            user = serializer.validated_data['user']

            # Send OTP after successful authentication (this is part of your flow)
            otp_instance = send_otp_email(user)

            # Generate JWT tokens after OTP is sent
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            # Create response object
            response = Response(
                {
                    'message':
                    'Login successful. OTP has been sent to your email.',
                    'otp_expiration':
                    otp_instance.expired_at.isoformat(),  # OTP expiration time
                    'user_id':
                    user.id  # Pass user ID for OTP verification step
                },
                status=status.HTTP_200_OK)

            # Set the tokens in HTTP-only cookies
            response = set_jwt_cookie(response, str(access_token),
                                      str(refresh))

            return response
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# OTP Login Verify View
class OTPLoginVerifyView(APIView):

    def post(self, request):
        # Deserialize the OTP verification data using the OTPVerifySerializer
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            otp_code = serializer.validated_data['otp']
            user_id = request.data.get('user_id')

            try:
                user = User.objects.get(id=user_id)

                # Fetch the latest OTP for the user
                otp_instance = OTP.objects.filter(
                    user=user, otp=otp_code).latest('created_at')

                if otp_instance.is_expired():
                    return Response({'error': 'OTP has expired'},
                                    status=status.HTTP_400_BAD_REQUEST)

                # Generate JWT tokens upon successful OTP verification
                refresh = RefreshToken.for_user(user)
                access_token = refresh.access_token

                # Create response object
                response = Response(
                    {
                        'message':
                        'OTP verified successfully. Login complete.',
                        'access_token':
                        str(access_token),  # This will be sent as a cookie
                        'refresh_token': str(
                            refresh)  # This will also be sent as a cookie
                    },
                    status=status.HTTP_200_OK)

                # Set the tokens in HTTP-only cookies
                response = set_jwt_cookie(response, str(access_token),
                                          str(refresh))

                return response

            except User.DoesNotExist:
                return Response({'error': 'Invalid user ID'},
                                status=status.HTTP_400_BAD_REQUEST)
            except OTP.DoesNotExist:
                return Response({'error': 'Invalid OTP'},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Token Refresh View
class TokenRefreshView(APIView):
    permission_classes = []  # Allow anyone to refresh the token

    def post(self, request):
        # Get the refresh token from the cookies
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({'error': 'Refresh token missing'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verify the refresh token and generate a new access token
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token

            # Return the new access token
            return Response({'access_token': str(access_token)},
                            status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'Invalid or expired refresh token'},
                            status=status.HTTP_400_BAD_REQUEST)


# Send OTP View (for logged-in users)
class SendOTPView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request):
        user = request.user
        otp_instance = send_otp_email(user)

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

                return Response({'message': 'OTP verified successfully'},
                                status=status.HTTP_200_OK)

            except OTP.DoesNotExist:
                return Response({'error': 'Invalid OTP'},
                                status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
