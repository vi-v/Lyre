# Generated by Django 2.0.5 on 2018-06-06 04:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20180603_1920'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='audio_format',
            field=models.CharField(default='\\ ', max_length=10),
            preserve_default=False,
        ),
    ]
