from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class RegisterTestCase(APITestCase):
    def test_register(self):
        data = {
            'username': 'testcase',
            'email': 'test@gmail.com',
            'password': 'NewPassword@123',
            'password2': 'NewPassword@123',
        }
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# upper class nothing can do below class, there are no dependancies
class LoginLogoutTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='example',
                                            password='NewPassword@123')
        
    def test_login(self):
        data = {
            'username': 'example',
            'password': 'NewPassword@123'
        }
        response = self.client.post(reverse('login'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
