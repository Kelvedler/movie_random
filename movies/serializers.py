from django.db import transaction
from rest_framework import serializers
from .models import (Movie, Photo, Review, Genre,
                     Persona, Director, Writer, Star)


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ['id', 'name']
        extra_kwargs = {'name': {'validators': []}}


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ['id', 'photo']


class MovieSerializer(serializers.ModelSerializer):
    genres = GenreSerializer(many=True, required=False)
    photos = PhotoSerializer(many=True, required=False)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'year', 'length', 'rating', 'trailer', 'description', 'genres', 'photos']

    def create(self, validated_data):
        with transaction.atomic():
            genres = validated_data.pop('genres')
            photos = validated_data.pop('photos')

            instance = Movie.objects.create(**validated_data)

            Photo.objects.bulk_create([Photo(**p, movie=instance) for p in photos])

            old_genres = Genre.objects.filter(name__in=[g['name'] for g in genres])
            new_genres = [Genre(**g) for g in genres if not g['name'] in [g.name for g in old_genres]]
            last_id = Genre.objects.last().id if Genre.objects.last() else 0
            for i in range(len(new_genres)):
                new_genres[i].id = last_id + 1
                last_id += 1
            new_genres = Genre.objects.bulk_create(new_genres)
            instance.genres.set([*new_genres, *old_genres])
        return instance

    def update(self, instance, validated_data):
        with transaction.atomic():
            genres = validated_data.pop('genres')
            photos = validated_data.pop('photos')

            instance = serializers.ModelSerializer.update(self, instance, validated_data)

            related_photos = Photo.objects.filter(movie_id=instance.id)
            related_photos.exclude(photo__in=[p['photo'] for p in photos]).delete()
            new_photos = [Photo(**p, movie=instance) for p in photos if not p['photo'] in [photo.photo for photo in related_photos]]
            Photo.objects.bulk_create(new_photos)

            old_genres = Genre.objects.filter(name__in=[g['name'] for g in genres])
            new_genres = [Genre(**g) for g in genres if not g['name'] in [g.name for g in old_genres]]
            last_id = Genre.objects.last().id if Genre.objects.last() else 0
            for i in range(len(new_genres)):
                new_genres[i].id = last_id + 1
                last_id += 1
            new_genres = Genre.objects.bulk_create(new_genres)
            instance.genres.set([*new_genres, *old_genres])
        return instance


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ['id', 'movie', 'title', 'review', 'user']
        read_only_fields = ['posted_at', ]
