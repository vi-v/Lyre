# Generated by Django 2.0.5 on 2018-05-29 05:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20180529_0458'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='album_name',
        ),
        migrations.RemoveField(
            model_name='song',
            name='artist_name',
        ),
    ]
