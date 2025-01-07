from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from django.core import mail


class UserAuthTests(APITestCase):

    def setUp(self):
        # Create a test user for registration
        self.user_data = {
            "username": "testuser",
            "email": "testuser@example.com",
            "password": "strongpassword123"
        }
        self.login_data = {
            "username": "testuser",
            "password": "strongpassword123"
        }
        self.otp_url = reverse(
            'send-otp')  # Assuming you defined your URL as 'send-otp'
        self.verify_otp_url = reverse(
            'verify-otp')  # Assuming you defined your URL as 'verify-otp'

    def test_user_registration(self):
        url = reverse('user-register')
        response = self.client.post(url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'],
                         'User created successfully!')
        self.assertEqual(response.data['user']['username'],
                         self.user_data['username'])

    def test_user_login(self):
        # First, register the user
        self.client.post(reverse('user-register'),
                         self.user_data,
                         format='json')

        # Now, login with the created user
        response = self.client.post(reverse('user-login'),
                                    self.login_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access_token', response.data)
        self.assertIn('refresh_token', response.data)

    def test_send_otp(self):
        # First, register and login the user
        self.client.post(reverse('user-register'),
                         self.user_data,
                         format='json')
        login_response = self.client.post(reverse('user-login'),
                                          self.login_data,
                                          format='json')
        access_token = login_response.data['access_token']

        # Request OTP with the authenticated user
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        response = self.client.post(self.otp_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('otp_expiration', response.data)

        # Check that an email was sent
        self.assertEqual(len(mail.outbox), 1)  # Ensure an email was sent
        self.assertIn('Your OTP Code',
                      mail.outbox[0].subject)  # Verify OTP subject

    def test_verify_otp(self):
        # First, register and login the user
        self.client.post(reverse('user-register'),
                         self.user_data,
                         format='json')
        login_response = self.client.post(reverse('user-login'),
                                          self.login_data,
                                          format='json')
        access_token = login_response.data['access_token']

        # Request OTP
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access_token)
        otp_response = self.client.post(self.otp_url, format='json')
        otp_code = otp_response.data['message'].split()[
            -1]  # Get OTP code from the message

        # Verify OTP
        verify_data = {"otp": otp_code}
        response = self.client.post(self.verify_otp_url,
                                    verify_data,
                                    format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'OTP verified successfully')
