from django.shortcuts import render
from django.db.models import Prefetch
from django.http import Http404
from rest_framework import generics, permissions, views, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import (Movie,
                     Photo, Review, Genre, Persona,
                     Director, Writer, Star)
from accounts.models import Account
from .serializers import (MovieSerializer,
                          ReviewSerializer, GenreSerializer, PersonaSerializer)


class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.prefetch_related('genres', 'photos', 'directors', 'writers', 'stars')
    serializer_class = MovieSerializer


class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.prefetch_related('genres', 'photos', 'directors', 'writers', 'stars')
    serializer_class = MovieSerializer


class GenreList(views.APIView):
    def get(self, request, format=None):
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True, fields=('id', 'name'))
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = GenreSerializer(data=request.data, fields=('id', 'name'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.prefetch_related('movies')
    serializer_class = GenreSerializer


class ReviewCreate(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        account_id = Token.objects.get(key=request.auth.key).user_id
        request.data['account_id'] = account_id
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetail(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Review.objects.get(pk=pk)
        except Review.DoesNotExist:
            raise Http404

    def put(self, request, pk, format=None):
        account_id = Token.objects.get(key=request.auth.key).user_id
        review = self.get_object(pk)
        if review.account_id != account_id:
            return Response({"message": "prohibited from changing other users review"}, status=status.HTTP_400_BAD_REQUEST)
        if 'movie_id' in request.data and review.movie_id != request.data['movie_id']:
            return Response({"message": "prohibited from changing movie"}, status=status.HTTP_400_BAD_REQUEST)
        request.data['account_id'] = review.account_id
        request.data['movie_id'] = review.movie_id
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        account_id = Token.objects.get(key=request.auth.key).user_id
        is_staff = Account.objects.get(id=account_id).is_staff
        review = self.get_object(pk)
        if not is_staff and review.account_id != account_id:
            return Response({"message": "prohibited from deleting other users review"}, status=status.HTTP_400_BAD_REQUEST)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieReviewList(generics.ListAPIView):

    def get_queryset(self):
        return super().get_queryset().filter(movie=self.kwargs['movie_id'])

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class AccountReviewList(generics.ListAPIView):

    def get_queryset(self):
        return super().get_queryset().filter(account=self.kwargs['account_id'])

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class PersonaList(views.APIView):
    def get(self, request, format=None):
        genres = Persona.objects.all()
        serializer = PersonaSerializer(genres, many=True, fields=('id', 'first_name', 'last_name', 'birthdate'))
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PersonaSerializer(data=request.data, fields=('id', 'first_name', 'last_name', 'birthdate'))
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PersonaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Persona.objects.prefetch_related('directors', 'writers', 'stars')
    serializer_class = PersonaSerializer