import os
import re
import mimetypes
from uuid import uuid4
from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings
from core.models import Song
from media.models import EphemeralEntry


# Create your views here.

@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes(api_settings.DEFAULT_AUTHENTICATION_CLASSES)
def get_song_key(request, song_id):
    try:
        song = Song.objects.get(pk=song_id)
        ephemeral_key = str(uuid4())
        entry = EphemeralEntry(
            song=song,
            key=ephemeral_key
        )
        entry.save()
        return HttpResponse(ephemeral_key)
    except ObjectDoesNotExist:
        raise Http404('song does not exist')


@api_view(['GET'])
@permission_classes((IsAuthenticated, ))
@authentication_classes(api_settings.DEFAULT_AUTHENTICATION_CLASSES)
def stream_song(request, song_key):
    try:
        entry = EphemeralEntry.objects.get(key=song_key)
    except ObjectDoesNotExist:
        raise Http404()

    try:
        song = entry.song
        entry.delete()

        range_header = request.META.get('Range')
        if not range_header:
            response = StreamingHttpResponse((line for line in open(song.path, 'rb')))
            response['Accept-Ranges'] = 'bytes'
            response['Content-Type'] = song.mime_type
            response['Content-Length'] = os.path.getsize(song.path)
            return response

        size = os.path.getsize(song.path)
        byte1, byte2 = 0, None

        m = re.search('(\d+)-(\d*)', range_header)
        g = m.groups()

        if g[0]:
            byte1 = int(g[0])
        if g[1]:
            byte2 = int(g[1])

        length = size - byte1
        if byte2 is not None:
            length = byte2 - byte1

        with open(song.path, 'rb') as f:
            f.seek(byte1)
            data = f.read(length)

        response = HttpResponse(data, content_type=mimetypes.guess_type(song.path)[0])
        response['Accept-Ranges'] = 'bytes'
        response['Content-Range'] = 'bytes {0}-{1}/{2}'.format(byte1, byte1 + length - 1, size)
        response.status_code(206)
        return response
    except FileNotFoundError:
        raise Http404('file does not exist')
