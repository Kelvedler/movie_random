from django.db import transaction
from rest_framework import serializers
from .models import (Movie, Genre, GenreMovieMap,
                     Photo, Review, Persona,
                     Director, Writer, Star)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ['id', 'name']
        extra_kwargs = {'name': {'validators': []}}


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, required=False)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'year', 'length', 'rating', 'trailer', 'description', 'genres']

    def create(self, validated_data):
        with transaction.atomic():
            genres = validated_data.pop('genres')
            instance = Movie.objects.create(**validated_data)
            old_genres = Genre.objects.filter(name__in=[g['name'] for g in genres])
            new_genres = [Genre(**g) for g in genres if not g['name'] in [g.name for g in old_genres]]
            new_genres = Genre.objects.bulk_create(new_genres)
            instance.genres.set([*new_genres, *old_genres])
        return instance

    def update(self, instance, validated_data):
        with transaction.atomic():
            genres = validated_data.pop('genres')
            instance = serializers.ModelSerializer.update(self, instance, validated_data)
            old_genres = Genre.objects.filter(name__in=[g['name'] for g in genres])
            new_genres = [Genre(**g) for g in genres if not g['name'] in [g.name for g in old_genres]]
            new_genres = Genre.objects.bulk_create(new_genres)
            instance.genres.set([*new_genres, *old_genres])
        return instance


class GenreMovieMapSerializer(serializers.ModelSerializer):
    genre = GenreSerializer()
    movie = MovieSerializer()

    class Meta:
        model = GenreMovieMap
        fields = ['genre', 'movie']
