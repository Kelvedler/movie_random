from django.db import models


class Movies(models.Model):
    title = models.CharField(max_length=200)
    year = models.PositiveSmallIntegerField()
    length = models.PositiveSmallIntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    trailer = models.URLField()
    description = models.CharField(max_length=600)


class Genres(models.Model):
    genre = models.CharField(max_length=40)


class GenreMovieMap(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)


class Photos(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    photo = models.URLField()


class Reviews(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    user = models.ForeignKey('accounts.Users', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    review = models.CharField(max_length=4000)
    posted_at = models.DateField(auto_now_add=True)


class Personas(models.Model):
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    birthdate = models.DateField()
    biography = models.CharField(max_length=4000)


class Directors(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    persona = models.ForeignKey(Personas, on_delete=models.CASCADE)


class Writers(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    persona = models.ForeignKey(Personas, on_delete=models.CASCADE)
    type = models.CharField(max_length=40)


class Stars(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE)
    persona = models.ForeignKey(Personas, on_delete=models.CASCADE)
    character = models.CharField(max_length=80)
