from rest_framework import serializers
from .models import (Movie, Genre, GenreMovieMap,
                     Photo, Review, Persona,
                     Director, Writer, Star)


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = [
            'pk', 'title', 'year', 'length',
            'rating', 'trailer', 'description',
        ]
