from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from actors.models import Actor
from genres.models import Genre
from movies.models import Movie
from reviews.models import Review


class MovieAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='admin12345')
        self.client.force_authenticate(self.user)
        self.genre = Genre.objects.create(name='Ficção')
        self.actor = Actor.objects.create(name='Ator Teste')

    def _payload(self, **overrides):
        data = {
            'title': 'Matrix',
            'genre': self.genre.id,
            'release_date': '1999-03-31',
            'actors': [self.actor.id],
            'resume': 'Um hacker descobre a verdade.',
        }
        data.update(overrides)
        return data

    def test_create_movie(self):
        response = self.client.post('/api/v1/movies/', self._payload())

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Movie.objects.count(), 1)

    def test_release_date_before_1990_is_invalid(self):
        response = self.client.post('/api/v1/movies/', self._payload(release_date='1985-01-01'))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_resume_longer_than_200_is_invalid(self):
        response = self.client.post('/api/v1/movies/', self._payload(resume='x' * 201))

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_movie_rate_is_average_of_reviews(self):
        movie = Movie.objects.create(title='Matrix', genre=self.genre)
        Review.objects.create(movie=movie, stars=4)
        Review.objects.create(movie=movie, stars=5)

        response = self.client.get(f'/api/v1/movies/{movie.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['rate'], 4.5)

    def test_stats(self):
        movie = Movie.objects.create(title='Matrix', genre=self.genre)
        Review.objects.create(movie=movie, stars=5)

        response = self.client.get('/api/v1/movies/stats/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['movies_total'], 1)
        self.assertEqual(response.data['reviews_total'], 1)
        self.assertEqual(response.data['average_stars'], 5.0)

    def test_requires_authentication(self):
        self.client.force_authenticate(None)
        response = self.client.get('/api/v1/movies/')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
