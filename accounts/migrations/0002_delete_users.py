# Generated by Django 3.2 on 2021-06-29 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authtoken', '0003_tokenproxy'),
        ('movies', '0016_alter_review_user'),
        ('admin', '0003_logentry_add_action_flag_choices'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Users',
        ),
    ]