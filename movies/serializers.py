from rest_framework import serializers
from django.db.models import Avg

from movies.models import Movie
# from genres.models import Genre
# from actors.models import Actor


# apenas um exemplo de como criar um Serializer manualmente.
# temos q fazer tudo na "mão". este por exemplo, não grava registro pq nao foi criado o metodo "Create()""
# class MovieSerializer(serializers.Serializer):
#     title = serializers.CharField()
#     genre = serializers.PrimaryKeyRelatedField(
#         queryset=Genre.objects.all()
#     )
#     release_date = serializers.DateField()
#     actors = serializers.PrimaryKeyRelatedField(
#         queryset=Actor.objects.all(),
#         many=True
#     )
#     resume = serializers.CharField()


class MovieModelSerializer(serializers.ModelSerializer):
    rate = serializers.SerializerMethodField(read_only=True)  # Campo calculado

    class Meta:
        model = Movie
        fields = '__all__'  # ou ['title']

    def get_rate(self, obj):  # o obj é cada um dos registros retornados
        rate = obj.reviews.aggregate(Avg('stars'))['stars__avg']   # aggregate é para adicionar um campo no retorno do sql

        if rate:
            return round(rate, 1)

        return None

        # reviews = obj.reviews.all()   O obj é o movie
        #                               este "reviews" no obj é o nome da relação que foi dada no models de Reviews. é o nome do
        #                             # relacionamento. related_name='reviews'. Ele funciona como uma query.
        # if reviews:
        #     sum_reviews = 0
        #     for review in reviews:
        #         sum_reviews += review.stars

        #     reviews_count = reviews.count()

        #     return round(sum_reviews / reviews_count, 1)

        # return None

    def validate_release_date(self, value):
        if value.year < 1990:
            raise serializers.ValidationError('A data de lançamento não pode ser menor que 1990!')

        return value

    def validate_resume(self, value):
        if len(value) > 500:
            raise serializers.ValidationError('Resumo deve ter no máximo 200 caracteres!')

        return value
