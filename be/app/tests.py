from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, BlogPost


class AuthAndBlogAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('auth_register')
        self.login_url = reverse('auth_login')
        self.logout_url = reverse('auth_logout')
        self.me_url = reverse('auth_me')
        self.refresh_url = reverse('token_refresh')
        self.blog_url = reverse('blog_list_create')

        self.user_data = {
            'username': 'john_doe',
            'email': 'john@example.com',
            'password': 'password123',
            'password_confirm': 'password123',
            'role': 'user'
        }

    def test_registration(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['user']['username'], 'john_doe')
        self.assertEqual(response.data['user']['email'], 'john@example.com')
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])

    def test_login_with_username(self):
        self.client.post(self.register_url, self.user_data, format='json')
        login_data = {
            'username': 'john_doe',
            'password': 'password123'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['email'], 'john@example.com')

    def test_login_with_email(self):
        self.client.post(self.register_url, self.user_data, format='json')
        login_data = {
            'username': 'john@example.com',
            'password': 'password123'
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_create_blog_post_authenticated(self):
        reg_resp = self.client.post(self.register_url, self.user_data, format='json')
        access_token = reg_resp.data['tokens']['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

        post_data = {
            'title': 'My First Post',
            'content': 'This is the full markdown/text content of the blog post.',
        }
        response = self.client.post(self.blog_url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'My First Post')
        self.assertEqual(response.data['author']['username'], 'john_doe')


    def test_create_blog_post_unauthenticated_fails(self):
        post_data = {
            'title': 'Unauthorized Post',
            'content': 'Should fail without auth.'
        }
        response = self.client.post(self.blog_url, post_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
