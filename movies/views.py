from django.shortcuts import render
from rest_framework import generics, permissions
from .models import (Movie, Genre, GenreMovieMap,
                     Photo, Review, Persona,
                     Director, Writer, Star)
from .serializers import MovieSerializer, GenreSerializer


class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.prefetch_related('genres', 'photos')
    serializer_class = MovieSerializer


class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.prefetch_related('genres', 'photos')
    serializer_class = MovieSerializer


class GenreList(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
