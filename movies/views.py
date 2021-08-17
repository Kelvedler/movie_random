from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from .models import Movie, Review, Genre, Persona
from accounts.models import Account
from .serializers import MovieSerializer, ReviewSerializer, GenreSerializer, PersonaSerializer


class MovieList(generics.ListCreateAPIView):
    queryset = Movie.objects.prefetch_related('genres', 'photos', 'directors', 'writers', 'stars')
    serializer_class = MovieSerializer


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


class GenreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.prefetch_related('movies')
    serializer_class = GenreSerializer


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

    def put(self, request, *args, **kwargs):
        account_id = Token.objects.get(key=request.auth.key).user_id
        review = self.get_object()
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

    def delete(self, request, *args, **kwargs):
        account_id = Token.objects.get(key=request.auth.key).user_id
        is_staff = Account.objects.get(id=account_id).is_staff
        review = self.get_object()
        if not is_staff and review.account_id != account_id:
            return Response({"message": "prohibited from deleting other users review"}, status=status.HTTP_400_BAD_REQUEST)
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MovieReviewList(generics.ListAPIView):

    def get_queryset(self):
        return super().get_queryset().filter(movie=self.kwargs['movie_id'])

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['fields'] = ['id', 'title', 'review', 'account_id']
        return serializer_class(*args, **kwargs)


class AccountReviewList(generics.ListAPIView):

    def get_queryset(self):
        return super().get_queryset().filter(account=self.kwargs['account_id'])

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs['fields'] = ['id', 'title', 'review', 'movie_id']
        return serializer_class(*args, **kwargs)


class PersonaList(generics.ListCreateAPIView):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        if self.request.method == 'GET':
            kwargs['fields'] = ['id', 'first_name', 'last_name', 'birthdate']
        else:
            kwargs['fields'] = ['id', 'first_name', 'last_name', 'birthdate', 'biography']
        return serializer_class(*args, **kwargs)


class PersonaDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Persona.objects.prefetch_related('directors', 'writers', 'stars')
    serializer_class = PersonaSerializer
