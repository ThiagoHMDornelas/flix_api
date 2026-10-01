from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.test import APITestCase

from genres.models import Genre
from movies.models import Movie
from reviews.models import Review


class ReviewAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_superuser(username='admin', password='admin12345')
        self.client.force_authenticate(self.user)
        self.genre = Genre.objects.create(name='Drama')
        self.movie = Movie.objects.create(title='Filme Teste', genre=self.genre)

    def test_create_review(self):
        response = self.client.post('/api/v1/reviews/', {
            'movie': self.movie.id,
            'stars': 5,
            'comment': 'Ótimo filme!',
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Review.objects.count(), 1)

    def test_review_above_five_stars_is_invalid(self):
        response = self.client.post('/api/v1/reviews/', {
            'movie': self.movie.id,
            'stars': 6,
        })

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_review_below_zero_stars_is_invalid(self):
        review = Review(movie=self.movie, stars=-1)

        with self.assertRaises(ValidationError):
            review.full_clean()
