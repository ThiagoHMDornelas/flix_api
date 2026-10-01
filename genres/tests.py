from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from genres.models import Genre


class GenreAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='admin12345')
        self.client.force_authenticate(self.user)
        self.genre = Genre.objects.create(name='Ação')

    def test_str(self):
        self.assertEqual(str(self.genre), 'Ação')

    def test_list_genres(self):
        response = self.client.get('/api/v1/genres/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_genre(self):
        response = self.client.post('/api/v1/genres/', {'name': 'Drama'})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Genre.objects.filter(name='Drama').exists())

    def test_requires_authentication(self):
        self.client.force_authenticate(None)
        response = self.client.get('/api/v1/genres/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
