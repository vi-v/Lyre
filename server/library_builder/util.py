import os


def is_audio_file(filename):
    audio_extensions = [
        '.mp3',
        '.mp4',
        '.wav',
        '.flac'
    ]

    name, file_extension = os.path.splitext(filename)

    return file_extension in audio_extensions
