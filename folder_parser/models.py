from mutagen.id3 import APIC
import hashlib
import base64


class Song:
    def __init__(self, title, path, start_time, duration, end_time=None, album='Unknown', artist='Unknown', **kwargs):
        self.title = title
        self.path = path
        self.duration = duration
        self.start_time = start_time
        self.end_time = end_time or self.start_time + self.duration
        self.artist = artist
        self.album = album

        if self.artist == 'Unknown' and 'TPE1' in kwargs:
            self.artist = str(kwargs['TPE1'])

        if self.album == 'Unknown' and 'TALB' in kwargs:
            self.album = str(kwargs['TALB'])

        for key, value in kwargs.items():
            setattr(self, key, value)

    def album_hash(self):
        _str = self.album.lower().strip() + self.artist.lower().strip()
        return hashlib.md5(str.encode(_str)).hexdigest()

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


class Folder:
    def __init__(self, path):
        self.path = path
        self.num_tracks = 0
        self.tracks = []

    def add(self, file):
        if(isinstance(file, Song)):
            self.num_tracks += 1
            self.tracks.append(file)

    def pprint(self, verbose=False):
        _str = 'Folder (\n'

        for key in dir(self):
            attr = getattr(self, key)
            if not key.startswith('__') and not callable(attr):
                _str += '       {}={},\n'.format(key, attr)

        _str += ')'

        return _str


class Album:
    def __init__(self, title, artist, art=None):
        self.title = title
        self.artist = artist
        self.tracks = []
        self.num_tracks = 0
        self.art = art

    def add(self, file):
        if(isinstance(file, Song)):
            self.num_tracks += 1
            self.tracks.append(file)

        if(isinstance(file, APIC)):
            self.art = base64.b64encode(file.data)

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


class Artist:
    def __init__(self, name):
        self.name = name
        self.tracks = []
        self.num_tracks = 0
        self.albums = []
        self.num_albums = 0

    def add(self, obj):
        if isinstance(obj, Song):
            self.num_tracks += 1
            self.tracks.append(obj)

        if isinstance(obj, Album):
            self.num_albums += 1
            self.albums.append(obj)

    def pprint(self, verbose=False):
        _str = 'Artist (\n'

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
