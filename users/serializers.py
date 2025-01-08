from rest_framework import serializers
from django.contrib.auth.models import User
from .models import OTP, StudentProfile
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed


# Serializer for User Registration (signup)
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True
            },  # Ensure password is write-only
        }

    def create(self, validated_data):
        # Create a new user with the validated data
        user = User.objects.create_user(username=validated_data['username'],
                                        email=validated_data['email'],
                                        password=validated_data['password'])
        return user


# Serializer for User Login (Login with email and password)
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        # Get the user with the provided email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed('Invalid credentials')

        # Authenticate the user using their username and password
        user = authenticate(username=user.username, password=password)

        if user is None:
            raise AuthenticationFailed('Invalid credentials')

        data['user'] = user
        return data


# Serializer for OTP Verification (verify OTP during login)
class OTPVerifySerializer(serializers.Serializer):
    otp = serializers.CharField(max_length=6)


# Serializer for StudentProfile (used to get and update student's profile)
class StudentProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = StudentProfile
        fields = [
            'registration_number', 'profile_picture', 'name', 'email',
            'phone_number', 'college_or_school', 'address',
            'enrolled_course_duration', 'fees_left'
        ]


# Serializer for User with Verified Status (Including the Verified field)
class UserWithVerifiedSerializer(serializers.ModelSerializer):
    verified = serializers.BooleanField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'verified']

    def update(self, instance, validated_data):
        instance.verified = validated_data.get('verified', instance.verified)
        instance.save()
        return instance
