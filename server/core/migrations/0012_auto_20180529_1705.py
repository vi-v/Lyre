# Generated by Django 2.0.5 on 2018-05-29 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_song_folder'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='album',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='songs', to='core.Album'),
        ),
        migrations.AlterField(
            model_name='song',
            name='artist',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='songs', to='core.Artist'),
        ),
        migrations.AlterField(
            model_name='song',
            name='folder',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='songs', to='core.Folder'),
        ),
    ]
