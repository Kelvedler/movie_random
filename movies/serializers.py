from django.db import transaction
from django.db.models import Q
from rest_framework import serializers, validators
from .models import (Movie, Photo, Review, Genre,
                     Persona, Director, Writer, Star)
from accounts.models import Account


class DynamicFieldsModelSerializer(serializers.ModelSerializer):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields', None)

        super(DynamicFieldsModelSerializer, self).__init__(*args, **kwargs)

        if fields is not None:

            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)


class GenreListSerializer(serializers.ListSerializer):
    def to_internal_value(self, data):
        return [{"name": d} for d in data]


class NestedGenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ['id', 'name']
        extra_kwargs = {'name': {'validators': []}}
        list_serializer_class = GenreListSerializer


class PhotoListSerializer(serializers.ListSerializer):
    def to_internal_value(self, data):
        return [{"photo": d} for d in data]


class PhotoSerializer(serializers.ModelSerializer):

    class Meta:
        model = Photo
        fields = ['id', 'photo']
        list_serializer_class = PhotoListSerializer


class NestedPersonaSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Persona
        fields = ['id', 'first_name', 'last_name', 'birthdate', 'biography']


class MovieSerializer(serializers.ModelSerializer):
    persona_fields = 'id', 'first_name', 'last_name', 'birthdate'
    persona_filters = persona_columns = ['first_name', 'last_name', 'birthdate']

    genres = NestedGenreSerializer(many=True, required=False)
    photos = PhotoSerializer(many=True, required=False)
    directors = NestedPersonaSerializer(many=True, required=False, validators=[], fields=persona_fields)
    writers = NestedPersonaSerializer(many=True, required=False, validators=[], fields=persona_fields)
    stars = NestedPersonaSerializer(many=True, required=False, validators=[], fields=persona_fields)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'year', 'length', 'rating', 'trailer',
                  'description', 'genres', 'photos', 'directors', 'writers', 'stars']

    @staticmethod
    def new_and_old(model, validated_obj: list, filters: list, columns: list):
        """
        Receive model class, list of validated data of related model, list of filters and list of columns
        that are unique together. Check if validated objects already exist in model, bulk_create if dont.
        Return list of both new and old model instances.

        :param model: class
        :param validated_obj: list of validated data of related model
        :param filters: list of strings, length is equal to length of columns
        :param columns: list of strings
        :return: [*new_instances, *old_instances]
        """
        if len(filters) == 1:
            fltr = filters[0]
            col = columns[0]
            old_instances = model.objects.filter(**{fltr: [obj[col] for obj in validated_obj]})
            new_instances = [model(**obj) for obj in validated_obj if not obj[col] in [getattr(obj, col) for obj in old_instances]]
        else:
            if validated_obj:
                obj_q = Q()
                for obj in validated_obj:
                    obj_q |= Q(**{fltr: obj[col] for fltr, col in zip(filters, columns)})
                old_instances = model.objects.filter(obj_q)
            else:
                old_instances = []
            new_instances = [model(**data) for data in validated_obj if
                           not {c: data[c] for c in columns} in [{c: getattr(data, c) for c in columns} for data in
                                                                 old_instances]]

        last_id = model.objects.last().id if model.objects.last() else 0
        for i in range(len(new_instances)):
            new_instances[i].id = last_id + 1
            last_id += 1
        new_instances = model.objects.bulk_create(new_instances)
        return [*new_instances, *old_instances]

    def create(self, validated_data):
        with transaction.atomic():
            genres = validated_data.pop('genres')
            photos = validated_data.pop('photos')
            directors = validated_data.pop('directors')
            writers = validated_data.pop('writers')
            stars = validated_data.pop('stars')

            instance = Movie.objects.create(**validated_data)

            Photo.objects.bulk_create([Photo(**p, movie=instance) for p in photos])

            instance.genres.set(self.new_and_old(Genre, genres, ['name__in'], ['name']))

            instance.directors.set(self.new_and_old(Persona, directors, self.persona_filters, self.persona_columns))
            instance.writers.set(self.new_and_old(Persona, writers, self.persona_filters, self.persona_columns))
            instance.stars.set(self.new_and_old(Persona, stars, self.persona_filters, self.persona_columns))

        return instance

    def update(self, instance, validated_data):
        with transaction.atomic():
            genres = validated_data.pop('genres')
            photos = validated_data.pop('photos')
            directors = validated_data.pop('directors')
            writers = validated_data.pop('writers')
            stars = validated_data.pop('stars')

            instance = serializers.ModelSerializer.update(self, instance, validated_data)

            related_photos = Photo.objects.filter(movie_id=instance.id)
            related_photos.exclude(photo__in=[p['photo'] for p in photos]).delete()
            new_photos = [Photo(**p, movie=instance) for p in photos if not p['photo'] in [photo.photo for photo in related_photos]]
            Photo.objects.bulk_create(new_photos)

            instance.genres.set(self.new_and_old(Genre, genres, ['name__in'], ['name']))

            instance.directors.set(self.new_and_old(Persona, directors, self.persona_filters, self.persona_columns))
            instance.writers.set(self.new_and_old(Persona, writers, self.persona_filters, self.persona_columns))
            instance.stars.set(self.new_and_old(Persona, stars, self.persona_filters, self.persona_columns))
        return instance


class ReviewSerializer(serializers.ModelSerializer):
    movie_id = serializers.PrimaryKeyRelatedField(source='movie', queryset=Movie.objects.all())
    account_id = serializers.PrimaryKeyRelatedField(source='account', queryset=Account.objects.all())

    class Meta:
        model = Review
        fields = ['id', 'movie_id', 'title', 'review', 'account_id']
        read_only_fields = ['posted_at', ]


class NestedMovieSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Movie
        fields = ['id', 'title', 'year', 'length', 'rating', 'trailer', 'description']


class GenreSerializer(DynamicFieldsModelSerializer):
    movies = NestedMovieSerializer(many=True, required=False, fields=('id', 'title', 'year'))

    class Meta:
        model = Genre
        fields = ['id', 'name', 'movies']


class PersonaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Persona
        fields = ['id', 'first_name', 'last_name', 'birthdate', 'biography']
