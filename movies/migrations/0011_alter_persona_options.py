# Generated by Django 3.2 on 2021-08-17 20:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0010_auto_20210814_2352'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='persona',
            options={'ordering': ['last_name']},
        ),
    ]
