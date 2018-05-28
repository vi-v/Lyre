import sys
import os
import time
import logging
import mutagen
from watchdog.observers import Observer
from fshandler import FSHandler
from util import is_audio_file
from models import Song, Album, Artist, Folder

album_map = {}
artist_map = {}


def put_album_in_artist(album):
    if album.artist.lower() not in artist_map:
        artist = Artist(album.artist)
        artist.add(album)
        artist_map[album.artist.lower()] = artist


def put_song_in_album(song):
    if song.album_hash() not in album_map:
        album = Album(song.album, song.artist)
        album.add(song)
        try:
            album.add(getattr(song, 'APIC:'))
        except AttributeError:
            pass
        album_map[song.album_hash()] = album
    else:
        album = album_map[song.album_hash()]
        album.add(song)

    put_album_in_artist(album)


def put_song_in_artist(song):
    if song.artist.lower() not in artist_map:
        artist = Artist(song.artist)
        artist.add(song)
        artist_map[song.artist.lower()] = artist
    else:
        artist = artist_map[song.artist.lower()]
        artist.add(song)


def scan_directory(dirname):
    for root, subdirs, files in os.walk(dirname):
        folder = Folder(root)

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
                    start_time=0.0,
                    duration=metadata_file.info.length,
                    bitrate=metadata_file.info.bitrate,
                    sample_rate=metadata_file.info.sample_rate,
                    **metadata)

                put_song_in_album(song)
                put_song_in_artist(song)
                folder.add(song)

                # print(song.pprint(verbose=True))
                # print('\n')

        if folder.num_tracks != 0:
            print(folder.pprint())
            print('\n')

    for key, album in album_map.items():
        print(album.pprint())
        for song in album.tracks:
            print(song.pprint())

    for key, artist in artist_map.items():
        print(artist.pprint())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = FSHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    # observer.start()
    scan_directory(path)
    # try:
    #     while True:
    #         time.sleep(1)
    # except KeyboardInterrupt:
    #     observer.stop()
    # observer.join()
