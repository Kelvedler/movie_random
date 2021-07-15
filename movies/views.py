from django.shortcuts import render
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
        user_id = Token.objects.get(key=request.auth.key).user_id
        request.data['user'] = user_id
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
        user_id = Token.objects.get(key=request.auth.key).user_id
        review = self.get_object(pk)
        if review.user_id != user_id:
            return Response({"message": "prohibited from changing other users review"}, status=status.HTTP_400_BAD_REQUEST)
        if 'movie' in request.data and review.movie_id != request.data['movie']:
            return Response({"message": "prohibited from changing movie"}, status=status.HTTP_400_BAD_REQUEST)
        request.data['user'] = review.user_id
        request.data['movie'] = review.movie_id
        serializer = ReviewSerializer(review, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        user_id = Token.objects.get(key=request.auth.key).user_id
        is_staff = Account.objects.get(id=user_id).is_staff
        review = self.get_object(pk)
        if not is_staff and review.user_id != user_id:
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
        return super().get_queryset().filter(user=self.kwargs['account_id'])

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class PersonaList(generics.ListCreateAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer


class PersonaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer