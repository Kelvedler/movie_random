# Generated by Django 3.2 on 2021-06-18 19:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0005_movie_genres'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='genres',
        ),
    ]
