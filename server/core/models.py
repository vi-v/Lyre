from django.db import models
from mutagen.id3 import APIC
import hashlib
import base64
import pickle

# Create your models here.


class Artist(models.Model):
	_id = models.AutoField(primary_key=True)
	name = models.CharField(200)
	track_ids = models.CharField(100000)
	num_tracks = models.IntegerField(default=0)
	album_ids = models.CharField(100000)
	num_albums = models.IntegerField(default=0)


class Album(models.Model):
	_id = models.AutoField(primary_key=True)
	name = models.CharField(200)
	artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
	track_ids = models.CharField(100000)
	num_tracks = models.IntegerField(default=0)
	art = models.CharField(50000)

	def add(self, item):
		if(isinstance(item, Song)):
			self.num_tracks += 1
			ids = pickle.loads(self.track_ids)
			ids.append(item._id)
			self.track_ids = pickle.dumps(ids)

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


class Folder(models.Model):
	_id = models.AutoField(primary_key=True)
	path = models.CharField(500)
	num_tracks = models.IntegerField(default=0)
	track_ids = models.CharField(100000)

	def add(self, item):
		if isinstance(item, Song):
			self.num_tracks += 1
			ids = pickle.loads(self.track_ids)
			ids.append(item._id)
			self.track_ids = pickle.dumps(ids)
		
		self.save()

	def pprint(self, verbose=False):
		_str = 'Folder (\n'

		for key in dir(self):
			attr = getattr(self, key)
			if not key.startswith('__') and not callable(attr):
				_str += '       {}={},\n'.format(key, attr)

		_str += ')'

		return _str


class Song(models.Model):
	_id = models.AutoField(primary_key=True)
	title = models.CharField(200)
	path = models.CharField(200)
	duration = models.FloatField(default=0)
	start_time = models.FloatField(default=0)
	end_time = models.FloatField(default=0)
	artist_name = models.CharField(200)
	artist = models.ForeignKey(Album, on_delete=models.CASCADE)
	album_name = models.CharField(200)
	album = models.ForeignKey(Artist, on_delete=models.CASCADE)

	# Metadata using the ID3v2 standard
	TALB = models.CharField(200)
	TCON = models.CharField(200)
	TCOP = models.CharField(400)
	TDRC = models.CharField(200)
	TIT2 = models.CharField(200)
	TOPE = models.CharField(200)
	TPE1 = models.CharField(200)
	TPE2 = models.CharField(200)
	TRCK = models.IntegerField(default=0)
	WXXX = models.CharField(200)

	def album_hash(self):
		_str = self.album_name.lower().strip() + self.artist_name.lower().strip()
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
