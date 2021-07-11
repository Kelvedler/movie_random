from django.contrib import admin
from .models import Movie, Photo, Review, Director, Writer, Star, Genre, GenreMovieMap

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(GenreMovieMap)
admin.site.register(Photo)
admin.site.register(Review)
admin.site.register(Director)
admin.site.register(Writer)
admin.site.register(Star)
