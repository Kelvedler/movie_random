from django.db import models
from accounts.models import Account


class Genre(models.Model):
    name = models.CharField(max_length=40, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Persona(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    birthdate = models.DateField()
    biography = models.CharField(max_length=4000, blank=True)

    class Meta:
        unique_together = ['first_name', 'last_name', 'birthdate']
        ordering = ['last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name} {self.birthdate.strftime("%Y-%m-%d")}'


class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField()
    length = models.PositiveSmallIntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    trailer = models.URLField()
    description = models.CharField(max_length=600)
    genres = models.ManyToManyField(Genre, through='GenreMovieMap', related_name='movies')
    directors = models.ManyToManyField(Persona, through='Director', related_name='directors')
    writers = models.ManyToManyField(Persona, through='Writer', related_name='writers')
    stars = models.ManyToManyField(Persona, through='Star', related_name='stars')

    class Meta:
        unique_together = ['title', 'year']
        ordering = ['title']

    def __str__(self):
        return f'{self.title}, {self.year}'


class GenreMovieMap(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['movie', 'genre']

    def __str__(self):
        return f'{self.genre} {self.movie}'


class Photo(models.Model):
    movie = models.ForeignKey(Movie, related_name='photos', on_delete=models.CASCADE)
    photo = models.URLField()

    def __str__(self):
        return f'{self.movie}: photo {self.id}'


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    review = models.CharField(max_length=4000)
    posted_at = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ['account', 'movie']
        ordering = ['title']

    def __str__(self):
        return self.title


class Director(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.persona} in {self.movie}'


class Writer(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.persona} in {self.movie}'


class Star(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.persona} in {self.movie}'
