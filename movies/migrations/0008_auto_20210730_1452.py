# Generated by Django 3.2 on 2021-07-30 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0007_auto_20210730_1412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='star',
            name='character',
            field=models.CharField(blank=True, max_length=80),
        ),
        migrations.AlterField(
            model_name='writer',
            name='type',
            field=models.CharField(blank=True, max_length=40),
        ),
    ]