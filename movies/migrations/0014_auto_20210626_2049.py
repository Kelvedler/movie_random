# Generated by Django 3.2 on 2021-06-26 17:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0013_alter_genre_genre'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genre',
            options={'ordering': ['name']},
        ),
        migrations.RenameField(
            model_name='genre',
            old_name='genre',
            new_name='name',
        ),
    ]