from django.contrib import admin
from .models import Movie, Photo, Review, Director, Writer, Star, Genre, GenreMovieMap, Persona


class GenreInLine(admin.TabularInline):
    model = Genre.movies.through


class PhotoInLine(admin.TabularInline):
    model = Photo


class DirectorInLine(admin.TabularInline):
    model = Persona.directors.through


class WriterInLine(admin.TabularInline):
    model = Persona.writers.through


class StarInLine(admin.TabularInline):
    model = Persona.stars.through


class MovieInLine(admin.TabularInline):
    model = Movie.genres.through


class MovieAdmin(admin.ModelAdmin):
    inlines = [
        GenreInLine, PhotoInLine, DirectorInLine, WriterInLine, StarInLine
    ]
    list_display = ('title', 'year', 'rating', 'genre')

    def genre(self, obj):
        return [g.name for g in obj.genres.all()]


class GenreAdmin(admin.ModelAdmin):
    inlines = [
        MovieInLine,
    ]


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'account', 'movie')
    list_filter = ['account', 'movie']


class PersonaAdmin(admin.ModelAdmin):
    inlines = [
        DirectorInLine, WriterInLine, StarInLine
    ]


admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Persona, PersonaAdmin)
