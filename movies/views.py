from django.shortcuts import render
from rest_framework import generics, permissions
from .models import (Movie, Genre, GenreMovieMap,
                     Photo, Review, Persona,
                     Director, Writer, Star)
from .serializers import MovieSerializer


class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer


class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer
