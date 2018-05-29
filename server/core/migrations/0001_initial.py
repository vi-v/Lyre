# Generated by Django 2.0.5 on 2018-05-28 01:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('track_ids', models.CharField(max_length=100000)),
                ('num_tracks', models.IntegerField(default=0)),
                ('art', models.CharField(max_length=50000)),
            ],
        ),
        migrations.CreateModel(
            name='Artist',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('track_ids', models.CharField(max_length=100000)),
                ('num_tracks', models.IntegerField(default=0)),
                ('album_ids', models.CharField(max_length=100000)),
                ('num_albums', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Folder',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False)),
                ('path', models.CharField(max_length=500)),
                ('num_tracks', models.IntegerField(default=0)),
                ('track_ids', models.CharField(max_length=100000)),
            ],
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('_id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=200)),
                ('path', models.CharField(max_length=200)),
                ('duration', models.FloatField(default=0)),
                ('start_time', models.FloatField(default=0)),
                ('end_time', models.FloatField(default=0)),
                ('artist_name', models.CharField(max_length=200)),
                ('album_name', models.CharField(max_length=200)),
                ('TALB', models.CharField(max_length=200)),
                ('TCON', models.CharField(max_length=200)),
                ('TCOP', models.CharField(max_length=400)),
                ('TDRC', models.CharField(max_length=200)),
                ('TIT2', models.CharField(max_length=200)),
                ('TOPE', models.CharField(max_length=200)),
                ('TPE1', models.CharField(max_length=200)),
                ('TPE2', models.CharField(max_length=200)),
                ('TRCK', models.IntegerField(default=0)),
                ('WXXX', models.CharField(max_length=200)),
                ('album', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Artist')),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Album')),
            ],
        ),
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.Artist'),
        ),
    ]