import os
import mutagen
import base64
from watchdog.observers import Observer
from tqdm import tqdm
from django.core.exceptions import ObjectDoesNotExist
from core.models import Song, Album, Artist, Folder
from library_builder.fshandler import FSHandler
from library_builder.util import is_audio_file, md5


def scan_directory(dirname, silent=False):
	scanned_songs = 0
	scanned_albums = 0
	scanned_artists = 0
	scanned_folders = 0

	def do_walk(root, subdirs, files, pbar=None):
		scanned_songs = 0
		scanned_albums = 0
		scanned_artists = 0
		scanned_folders = 0

		folder = None

		for file in files:
			if is_audio_file(file):
				# Get folder for the song
				try:
					folder = Folder.objects.get(path=root)
				except ObjectDoesNotExist:
					folder = Folder(path=root)
					folder.save()
					scanned_folders += 1

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
						scanned_artists += 1
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
					album.save()
					scanned_albums += 1

				# Get album art
				if len(album.art) == 0 and 'APIC:' in metadata_file:
					apic = metadata_file['APIC:']
					album.art = base64.b64encode(apic.data).decode('utf-8')
					album.save()

				song, created = Song.objects.update_or_create(
					title=metadata.get('TIT2') or file,
					path=filepath,
					duration=metadata_file.info.length,
					start_time=0.0,
					end_time=metadata_file.info.length - 0.0,
					bitrate=metadata_file.info.bitrate,
					sample_rate=metadata_file.info.sample_rate,
					md5=md5(filepath),
					artist=artist,
					album=album,
					folder=folder,
					**metadata
				)
				scanned_songs += 1

				if pbar:
					pbar.update(1)

		return (scanned_songs, scanned_albums, scanned_artists, scanned_folders)
	
	if not silent:
		num_tracks = 0

		print("Scanning library...")

		for root, subdirs, files in os.walk(os.path.abspath(dirname)):
			for file in files:
				if is_audio_file(file):
					num_tracks += 1

		with tqdm(total=num_tracks, unit="files") as pbar:
			for root, subdirs, files in os.walk(os.path.abspath(dirname)):
				(_songs, _albums, _artists, _folders) = do_walk(root, subdirs, files, pbar=pbar)
				scanned_songs += _songs
				scanned_albums += _albums
				scanned_artists += _artists
				scanned_folders += _folders

		print('Created {} songs, {} albums, {} artists, and {} folders'
                    .format(scanned_songs, scanned_albums, scanned_artists, scanned_folders)
        )
		print()
	else:
		for root, subdirs, files in os.walk(os.path.abspath(dirname)):
			do_walk(root, subdirs, files)
		
