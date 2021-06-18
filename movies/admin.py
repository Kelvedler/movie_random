from django.contrib import admin
from .models import Movie, Genre, GenreMovieMap, Photo, Review, Director, Writer, Star

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(GenreMovieMap)
admin.site.register(Photo)
admin.site.register(Review)
admin.site.register(Director)
admin.site.register(Writer)
admin.site.register(Star)
