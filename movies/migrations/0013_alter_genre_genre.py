# Generated by Django 3.2 on 2021-06-21 19:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0012_alter_movie_genres'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='genre',
            field=models.CharField(max_length=40, unique=True),
        ),
    ]