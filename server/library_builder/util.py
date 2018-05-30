import os
import hashlib

def is_audio_file(filename):
    audio_extensions = [
        '.mp3',
        '.mp4',
        '.wav',
        '.flac'
    ]

    name, file_extension = os.path.splitext(filename)

    return file_extension in audio_extensions


def md5(filename):
    hash_md5 = hashlib.md5()
    with open(filename, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
