from rest_framework import serializers
from .models import (Movie, Genre, GenreMovieMap,
                     Photo, Review, Persona,
                     Director, Writer, Star)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ['id', 'genre']


class GenreMovieMapSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()

    class Meta:
        model = GenreMovieMap
        fields = ['genre']


class MovieSerializer(serializers.ModelSerializer):
    genres = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'year', 'length', 'rating', 'trailer', 'description', 'genres']

    def get_genres(self, obj):
        qset = GenreMovieMap.objects.filter(movie=obj)
        return [GenreMovieMapSerializer(g).data for g in qset]


