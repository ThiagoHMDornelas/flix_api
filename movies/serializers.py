from rest_framework import serializers
from django.db.models import Avg
from drf_spectacular.utils import extend_schema_field

from movies.models import Movie
from genres.serializers import GenreSerializer
from actors.serializers import ActorSerializer


class MovieListDetailSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()
    actors = ActorSerializer(many=True)
    rate = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'genre', 'actors', 'release_date', 'rate', 'resume']

    @extend_schema_field(serializers.FloatField(allow_null=True))
    def get_rate(self, obj):
        rate = obj.reviews.aggregate(Avg('stars'))['stars__avg']

        if rate:
            return round(rate, 1)

        return None


class MovieModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Movie
        fields = '__all__'

    def validate_release_date(self, value):
        if value.year < 1990:
            raise serializers.ValidationError('A data de lançamento não pode ser menor que 1990!')

        return value


class MovieStatsSerializer(serializers.Serializer):
    movies_total = serializers.IntegerField()
    movies_by_genre = serializers.ListField(child=serializers.DictField())
    reviews_total = serializers.IntegerField()
    average_stars = serializers.FloatField()
