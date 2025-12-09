from django.db.models import Count, Avg
from rest_framework import generics, views, response, status
from rest_framework.permissions import IsAuthenticated

from app.permissions import GlobalPermissionClass
from movies.models import Movie
from movies.serializers import MovieModelSerializer  # , MovieSerializer
from reviews.models import Review


class MovieCreateListView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, GlobalPermissionClass, )
    queryset = Movie.objects.all()
    serializer_class = MovieModelSerializer


class MovieRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, GlobalPermissionClass, )
    queryset = Movie.objects.all()
    serializer_class = MovieModelSerializer


class MovieStatsView(views.APIView):
    permission_classes = (IsAuthenticated, GlobalPermissionClass)
    queryset = Movie.objects.all()

    def get(self, request):
        movies_total = self.queryset.count()
        movies_by_genre = self.queryset.values('genre__name').annotate(count=Count('id'))
        reviews_total = Review.objects.count()
        average_stars = Review.objects.aggregate(avg_stars=Avg('stars'))['avg_stars']

        return response.Response(
            data={
                'movies_total': movies_total,
                'movies_by_genre': movies_by_genre,
                'reviews_total': reviews_total,
                'average_stars': round(average_stars, 1) if average_stars else 0,
            },
            status=status.HTTP_200_OK,
        )
