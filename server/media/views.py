import os
from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from core.models import Song

# Create your views here.


def stream_song(request, song_id):
    try:
        song = Song.objects.get(pk=song_id)

        try:
            response = StreamingHttpResponse(
                (line for line in open(song.path, 'rb')))
            response['Content-Type'] = song.mime_type
            response['Content-Length'] = os.path.getsize(song.path)
            return response
        except FileNotFoundError:
            raise Http404('file does not exist')
    except ObjectDoesNotExist:
        raise Http404('song does not exist')
