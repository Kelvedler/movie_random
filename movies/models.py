from django.db import models


class Genre(models.Model):
    genre = models.CharField(max_length=40, unique=True)

    class Meta:
        ordering = ['genre']

    def __str__(self):
        return self.genre


class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField()
    length = models.PositiveSmallIntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    trailer = models.URLField()
    description = models.CharField(max_length=600)
    genres = models.ManyToManyField(Genre, through='GenreMovieMap')

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
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    photo = models.URLField()

    def __str__(self):
        return self.photo


class Review(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.Users', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    review = models.CharField(max_length=4000)
    posted_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title


class Persona(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    birthdate = models.DateField()
    biography = models.CharField(max_length=4000)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Director(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)


class Writer(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    type = models.CharField(max_length=40)


class Star(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    character = models.CharField(max_length=80)
