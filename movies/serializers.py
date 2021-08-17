from django.db import transaction
from django.db.models import Q
from rest_framework import serializers
from .models import Movie, Photo, Review, Genre, Persona
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
    persona_columns = ['first_name', 'last_name', 'birthdate']

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
    def bulk_get_or_create__in(model, column: str, validated_obj: list):
        """
        Filter model column against the list of validated objects to either retrieve existing instances or create new.
        Return the list of both new and old instances.

        :param model: class
        :param column: string
        :param validated_obj: list of validated data of related model
        :return: [*new_instances, *old_instances]
        """
        old_instances = model.objects.filter(**{column + "__in": [obj[column] for obj in validated_obj]})
        new_instances = [model(**obj) for obj in validated_obj if
                         not obj[column] in [getattr(obj, column) for obj in old_instances]]

        last_id = model.objects.order_by('id').last().id if model.objects.last() else 0
        for i in range(len(new_instances)):
            new_instances[i].id = last_id + 1
            last_id += 1
        new_instances = model.objects.bulk_create(new_instances)
        return [*new_instances, *old_instances]

    @staticmethod
    def bulk_get_or_create_unique_together(model, columns: list, validated_obj: list):
        """
        Filter list of unique together columns in model against the list of validated objects
        to either retrieve existing instances or create new.
        Return the list of both new and old instances

        :param model: class
        :param columns: list of strings
        :param validated_obj: list of validated data of related model
        :return: [*new_instances, *old_instances]
        """
        if validated_obj:
            obj_q = Q()
            for obj in validated_obj:
                obj_q |= Q(**{col: obj[col] for col in columns})
            old_instances = model.objects.filter(obj_q)
        else:
            old_instances = []
        new_instances = [model(**data) for data in validated_obj if
                         not {c: data[c] for c in columns} in [{c: getattr(data, c) for c in columns} for data in
                                                               old_instances]]

        last_id = model.objects.order_by('id').last().id if model.objects.last() else 0
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

            instance.genres.set(self.bulk_get_or_create__in(Genre, 'name', genres))

            instance.directors.set(self.bulk_get_or_create_unique_together(Persona, self.persona_columns, directors))
            instance.writers.set(self.bulk_get_or_create_unique_together(Persona, self.persona_columns, writers))
            instance.stars.set(self.bulk_get_or_create_unique_together(Persona, self.persona_columns, stars))

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

            instance.genres.set(self.bulk_get_or_create__in(Genre, 'name', genres))

            instance.directors.set(self.bulk_get_or_create_unique_together(Persona, self.persona_columns, directors))
            instance.writers.set(self.bulk_get_or_create_unique_together(Persona, self.persona_columns, writers))
            instance.stars.set(self.bulk_get_or_create_unique_together(Persona, self.persona_columns, stars))
        return instance


class ReviewSerializer(DynamicFieldsModelSerializer):
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


class PersonaSerializer(DynamicFieldsModelSerializer):
    directors = NestedMovieSerializer(many=True, required=False, fields=('id', 'title', 'year'))
    writers = NestedMovieSerializer(many=True, required=False, fields=('id', 'title', 'year'))
    stars = NestedMovieSerializer(many=True, required=False, fields=('id', 'title', 'year'))

    class Meta:
        model = Persona
        fields = ['id', 'first_name', 'last_name', 'birthdate', 'biography', 'directors', 'writers', 'stars']
