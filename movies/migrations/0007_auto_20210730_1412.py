# Generated by Django 3.2 on 2021-07-30 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0006_auto_20210727_1956'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='stars',
            field=models.ManyToManyField(related_name='stars', through='movies.Star', to='movies.Persona'),
        ),
        migrations.AddField(
            model_name='movie',
            name='writers',
            field=models.ManyToManyField(related_name='writers', through='movies.Writer', to='movies.Persona'),
        ),
        migrations.AlterField(
            model_name='movie',
            name='directors',
            field=models.ManyToManyField(related_name='directors', through='movies.Director', to='movies.Persona'),
        ),
    ]
