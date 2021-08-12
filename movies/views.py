import datetime
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Movie, Review, Genre, Persona
from accounts.models import Account
from .serializers import MovieSerializer, ReviewSerializer, GenreSerializer, PersonaSerializer
from drf_spectacular.views import extend_schema
from drf_spectacular.utils import OpenApiExample


class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.prefetch_related('genres', 'photos', 'directors', 'writers', 'stars')
    serializer_class = MovieSerializer


@extend_schema(methods=['PATCH'], exclude=True)
class MovieDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Movie.objects.prefetch_related('genres', 'photos', 'directors', 'writers', 'stars')
    serializer_class = MovieSerializer


class GenreList(generics.ListCreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['fields'] = ['id', 'name']
        return serializer_class(*args, **kwargs)


@extend_schema(methods=['PATCH'], exclude=True)
class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.prefetch_related('movies')
    serializer_class = GenreSerializer


@extend_schema(description='account_id is taken from token', examples=[OpenApiExample(
    name='response', response_only=True,
    value={"id": 0, "movie_id": 0, "title": "string", "review": "string", "account_id": 0})])
class ReviewCreate(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['fields'] = ['id', 'movie_id', 'title', 'review']
        return serializer_class(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        account_id = Token.objects.get(key=request.auth.key).user_id
        request.data['account_id'] = account_id
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ReviewDetail(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    @extend_schema(examples=[OpenApiExample(name='request', request_only=True,
                                            value={"id": 0, "title": "string", "review": "string"})])
    def put(self, request, *args, **kwargs):
        account_id = Token.objects.get(key=request.auth.key).user_id
        review = self.get_object()
        if review.account_id != account_id:
            return Response({"message": "prohibited from changing other users review"}, status=status.HTTP_400_BAD_REQUEST)
        if 'movie_id' in request.data and review.movie_id != request.data['movie_id']:
            return Response({"message": "prohibited from changing movie"}, status=status.HTTP_400_BAD_REQUEST)
        request.data['account_id'] = review.account_id
        request.data['movie_id'] = review.movie_id
        serializer = ReviewSerializer(review, data=request.data, fields=['id', 'title', 'review'])
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        account_id = Token.objects.get(key=request.auth.key).user_id
        is_staff = Account.objects.get(id=account_id).is_staff
        review = self.get_object()
        if not is_staff and review.account_id != account_id:
            return Response({"message": "prohibited from deleting other users review"}, status=status.HTTP_400_BAD_REQUEST)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@extend_schema(examples=[OpenApiExample(
    name='response', response_only=True,
    value={"count": 123, "next": "http//api.example.org/movies/reviews/{movie_id}/?page=3",
           "previous": "http//api.example.org/movies/reviews/{movie_id}/?page=1",
           "results": [{"id": 0, "title": "string", "review": "string", "account_id": 0}]})])
class MovieReviewList(generics.ListAPIView):

    def get_queryset(self):
        return super().get_queryset().filter(movie=self.kwargs['movie_id'])

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['fields'] = ['id', 'title', 'review', 'account_id']
        return serializer_class(*args, **kwargs)


@extend_schema(examples=[OpenApiExample(
    name='response', response_only=True,
    value={"count": 123, "next": "http//api.example.org/movies/reviews/{account_id}/?page=3",
           "previous": "http//api.example.org/movies/reviews/{account_id}/?page=1",
           "results": [{"id": 0, "movie_id": 0, "title": "string", "review": "string"}]})])
class AccountReviewList(generics.ListAPIView):

    def get_queryset(self):
        return super().get_queryset().filter(account=self.kwargs['account_id'])

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['fields'] = ['id', 'title', 'review', 'movie_id']
        return serializer_class(*args, **kwargs)


@extend_schema(methods=['GET'], examples=[OpenApiExample(
    name='response', value={"count": 123, "next": "http//api.example.org/movies/personas/?page=3",
                            "previous": "http//api.example.org/movies/personas/?page=1", "results": [
            {"id": 0, "first_name": "string", "last_name": "string", "birthdate": datetime.date.today()}]})])
class PersonaList(generics.ListCreateAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = PersonaSerializer(queryset, many=True, fields=['id', 'first_name', 'last_name', 'birthdate'])
        return Response(serializer.data)

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['fields'] = ['id', 'first_name', 'last_name', 'birthdate', 'biography']
        return serializer_class(*args, **kwargs)


@extend_schema(methods=['PATCH'], exclude=True)
class PersonaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Persona.objects.prefetch_related('directors', 'writers', 'stars')
    serializer_class = PersonaSerializer
