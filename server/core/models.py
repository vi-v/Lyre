from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from mutagen.id3 import APIC
import hashlib
import base64
import json

# Create your models here.


class Artist(models.Model):
    _id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    num_tracks = models.IntegerField(default=0)
    num_albums = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Album(models.Model):
    _id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    num_tracks = models.IntegerField(default=0)
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, related_name='albums')
    art = models.CharField(max_length=50000, blank=True, default='')

    def add(self, item):
        if(isinstance(item, Song)):
            print("TODO: Add song")

        if(isinstance(item, APIC)):
            self.art = base64.b64encode(item.data)

        self.save()

    def pprint(self, verbose=False):
        _str = 'Album (\n'

        for key in dir(self):
            attr = getattr(self, key)
            if not key.startswith('__') and not callable(attr):
                if not verbose and isinstance(attr, bytes):
                    _str += '       {}={},\n'.format(key,
                                                     attr.decode('utf-8')[0:100] + '...')
                else:
                    _str += '       {}={},\n'.format(key, attr)
        _str += ')'

        return _str

    def __str__(self):
        return self.artist.name + ' - ' + self.name


@receiver(post_save, sender=Album)
def album_post_save(sender, created, instance, **kwargs):
    artist = Artist.objects.get(pk=instance.artist.pk)
    Artist.objects.select_for_update().filter(pk=artist.pk).update(
        num_albums=artist.albums.count()
    )


class Folder(models.Model):
    _id = models.AutoField(primary_key=True)
    path = models.CharField(max_length=500)
    num_tracks = models.IntegerField(default=0)

    def add(self, item):
        if isinstance(item, Song):
            print("TODO: Add song")

        self.save()

    def pprint(self, verbose=False):
        _str = 'Folder (\n'

        for key in dir(self):
            attr = getattr(self, key)
            if not key.startswith('__') and not callable(attr):
                _str += '       {}={},\n'.format(key, attr)

        _str += ')'

        return _str

    def __str__(self):
        return self.path


class Song(models.Model):
    _id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    path = models.CharField(max_length=200)
    duration = models.FloatField(default=0)
    start_time = models.FloatField(default=0)
    end_time = models.FloatField(default=0)
    bitrate = models.FloatField(default=0, blank=True)
    sample_rate = models.FloatField(default=0, blank=True)
    md5 = models.CharField(max_length=32, blank=True, default='')
    audio_format = models.CharField(max_length=10)
    mime_type = models.CharField(max_length=50)
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, default=0, related_name='songs')
    album = models.ForeignKey(
        Album, on_delete=models.CASCADE, null=True, blank=True, related_name='songs')
    folder = models.ForeignKey(
        Folder, on_delete=models.CASCADE, null=True, blank=True, related_name='songs')

    # Metadata using the ID3v2 standard
    TALB = models.CharField(max_length=200, blank=True, default='')
    TCON = models.CharField(max_length=200, blank=True, default='')
    TCOP = models.CharField(max_length=400, blank=True, default='')
    TDRC = models.CharField(max_length=200, blank=True, default='')
    TIT2 = models.CharField(max_length=200, blank=True, default='')
    TOPE = models.CharField(max_length=200, blank=True, default='')
    TPE1 = models.CharField(max_length=200, blank=True, default='')
    TPE2 = models.CharField(max_length=200, blank=True, default='')
    TRCK = models.IntegerField(blank=True, default=0)
    WXXX = models.CharField(max_length=200, blank=True, default='')

    def album_hash(self):
        _str = self.album.name.lower().strip() + self.artist.name.lower().strip()
        return hashlib.md5(str.encode(_str)).hexdigest()

    @staticmethod
    def metadata_keys():
        return [
            'TALB',
            'TCON',
            'TCOP',
            'TDRC',
            'TIT2',
            'TOPE',
            'TPE1',
            'TPE2',
            'TRCK',
            'WXXX'
        ]

    def pprint(self, verbose=False):
        _str = 'Song (\n'

        for key in dir(self):
            attr = getattr(self, key)
            if not key.startswith('__') and not callable(attr):
                if key == 'APIC:':
                    attr = attr.pprint()
                if verbose:
                    val = attr
                else:
                    if(len(str(attr)) > 100):
                        val = str(attr)[0:100] + '...'
                    else:
                        val = str(attr)

                _str += '       {}={},\n'.format(key, val)
        _str += ')'

        return _str

    def __str__(self):
        return self.artist.name + ' - ' + self.title


@receiver(post_save, sender=Song)
def song_post_save(sender, created, instance, **kwargs):
    # Update num_tracks of Artist, Album and Folder
    artist = Artist.objects.get(pk=instance.artist.pk)
    album = Album.objects.get(pk=instance.album.pk)
    folder = Folder.objects.get(pk=instance.folder.pk)

    Artist.objects.select_for_update().filter(pk=artist.pk).update(
        num_tracks=artist.songs.count()
    )
    Album.objects.select_for_update().filter(pk=album.pk).update(
        num_tracks=album.songs.count()
    )
    Folder.objects.select_for_update().filter(pk=folder.pk).update(
        num_tracks=folder.songs.count()
    )
    # instance.update()
