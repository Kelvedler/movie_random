from django.shortcuts import render
from rest_framework import generics, permissions, views, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
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


class ReviewCreate(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        user = Token.objects.get(key=request.auth.key).user_id
        request.data['user'] = user
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MovieReviewList(generics.ListAPIView):

    def get_queryset(self):
        return super().get_queryset().filter(movie=self.kwargs['movie_id'])

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class AccountReviewList(generics.ListAPIView):

    def get_queryset(self):
        return super().get_queryset().filter(user=self.kwargs['account_id'])

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
