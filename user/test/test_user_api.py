from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

def create_user(**params):
    return get_user_model().objects.create_user(**params)

class PublicUserApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        payload = {
            'email' : 'swati@abc.com',
            'password' : 'abcd',
            'name' : 'swati'
        }
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password',res.data)

    def test_user_exists(self):
        """"if user already exists"""
        payload = {
            'email': 'swati@abc.com',
            'password':'abcd'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL,payload)

        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """"check if password is too short"""
        payload = {
            'email' : 'swati@abc.com',
            'password':'pw'
        }
        res = self.client.post(CREATE_USER_URL,payload)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """"test if token is created for user"""
        payload = {
            'email' : 'swati@xyz.com',
            'password' : 'xyz'
                    }
        create_user(**payload)

        res=self.client.post(TOKEN_URL,payload)
        self.assertIn('token',res.date)
        self.assertEqual(res.status_code,status.HTTP_200_OK)

    def test_create_invalid_credentials(self):
        create_user( email='swati@xyz.com',password='xyz')
        payload = {
            'email' : 'swati@xyz.com',
            'password' : 'xyzabc'
        }
        res= self.client.post(TOKEN_URL,payload)
        self.assertNotIn('token',res.data)
        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

    # def test_create_token_no_user(self):
        """"Test that token is not created if user doesn't exist"""
