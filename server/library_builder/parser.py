import os
import mutagen
import base64
from watchdog.observers import Observer
from tqdm import tqdm
from django.core.exceptions import ObjectDoesNotExist
from core.models import Song, Album, Artist, Folder
from library_builder.fshandler import FSHandler
from library_builder.util import is_audio_file


def scan_directory(dirname):
	for root, subdirs, files in os.walk(os.path.abspath(dirname)):
		# Get folder for the song
		try:
			folder = Folder.objects.get(path=root)
		except ObjectDoesNotExist:
			folder = Folder(path=root)
			folder.save()

		for file in files:
			if is_audio_file(file):
				print(root, file)
				filepath = os.path.join(root, file)
				metadata_file = mutagen.File(filepath)

				metadata = {}
				for key in Song.metadata_keys():
					if key in metadata_file:
						metadata[key] = str(metadata_file.get(key))

				# Get artist for the song
				if 'TPE1' in metadata and len(metadata['TPE1']) != 0:
					try:
						artist = Artist.objects.get(
							name__iexact=metadata['TPE1'])
					except ObjectDoesNotExist:
						artist = Artist(name=metadata['TPE1'])
						artist.save()
				else:
					artist = Artist.objects.get(pk=0)

				# Get album for the song
				if 'TALB' in metadata:
					album_name = metadata['TALB']
				else:
					album_name = '<Unknown Album>'

				try:
					album = Album.objects.get(
						name__iexact=album_name,
						artist__name__iexact=artist.name
					)
				except ObjectDoesNotExist:
					album = Album(
						name=album_name,
						artist=artist
					)
					if 'APIC:' in metadata:
						apic = metadata['APIC:']
						album.art = base64.b64encode(apic.data)
					album.save()

				song = Song(
					title=metadata.get('TIT2') or file,
					path=filepath,
					duration=metadata_file.info.length,
					start_time=0.0,
					end_time=metadata_file.info.length - 0.0,
					bitrate=metadata_file.info.bitrate,
					sample_rate=metadata_file.info.sample_rate,
					artist=artist,
					album=album,
					folder=folder,
					**metadata
				)
				song.save()

		if folder.songs.count() == 0:
			folder.delete()
