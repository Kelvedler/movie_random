from django.shortcuts import render
from rest_framework import generics, permissions
from .models import (Movie,
                     Photo, Review, Genre, Persona,
                     Director, Writer, Star)
from .serializers import (MovieSerializer,
                          ReviewSerializer, GenreSerializer)


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


class MovieReviewList(generics.ListAPIView):

    def get_queryset(self):
        return super().get_queryset().filter(movie=self.kwargs['movie_id'])

    queryset = Review.objects.prefetch_related('movie', 'user')
    serializer_class = ReviewSerializer
