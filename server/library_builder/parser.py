import os
import mutagen
from core.models import Song, Album, Artist, Folder
from watchdog.observers import Observer
from library_builder.fshandler import FSHandler
from library_builder.util import is_audio_file

def scan_directory(dirname):
	for root, subdirs, files in os.walk(dirname):
		folder = Folder(
			path=root
		)

		for file in files:
			if is_audio_file(file):
				filepath = os.path.join(root, file)
				metadata_file = mutagen.File(filepath)

				metadata = {}
				for key in metadata_file.keys():
					metadata[key] = metadata_file.get(key)

				song = Song(
					title=metadata_file.get('TIT2') or file,
					path=filepath,
					duration=metadata_file.info.length,
					start_time=0.0,
					end_time=metadata_file.info.length - 0.0,
					bitrate=metadata_file.info.bitrate,
					sample_rate=metadata_file.info.sample_rate,
					**metadata)

				# put_song_in_album(song)
				# put_song_in_artist(song)
				folder.add(song)

				# print(song.pprint(verbose=True))
				# print('\n')

