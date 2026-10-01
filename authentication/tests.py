from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase


class AuthenticationAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='usuario', password='senha12345')

    def test_obtain_token(self):
        response = self.client.post('/api/v1/authentication/token/', {
            'username': 'usuario',
            'password': 'senha12345',
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_obtain_token_with_invalid_credentials(self):
        response = self.client.post('/api/v1/authentication/token/', {
            'username': 'usuario',
            'password': 'senha_errada',
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
