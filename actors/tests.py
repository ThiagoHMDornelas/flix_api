from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from actors.models import Actor


class ActorAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='admin12345')
        self.client.force_authenticate(self.user)

    def test_str(self):
        actor = Actor.objects.create(name='Julia Roberts')
        self.assertEqual(str(actor), 'Julia Roberts')

    def test_list_actors(self):
        Actor.objects.create(name='Sandra Bullock', nationality='USA')
        response = self.client.get('/api/v1/actors/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_actor(self):
        response = self.client.post('/api/v1/actors/', {
            'name': 'Wagner Moura',
            'birthday': '1976-06-27',
            'nationality': 'BRL',
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Actor.objects.filter(name='Wagner Moura').exists())

    def test_requires_authentication(self):
        self.client.force_authenticate(None)
        response = self.client.get('/api/v1/actors/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
