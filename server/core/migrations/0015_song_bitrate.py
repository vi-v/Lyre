# Generated by Django 2.0.5 on 2018-05-29 21:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0014_auto_20180529_1824'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='bitrate',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
