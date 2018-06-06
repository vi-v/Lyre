import os
from uuid import uuid4
from django.shortcuts import render
from django.http import StreamingHttpResponse, HttpResponse, Http404
from django.core.exceptions import ObjectDoesNotExist
from core.models import Song
from media.models import EphemeralEntry

# Create your views here.

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


def stream_song(request, song_key):
	try:
		entry = EphemeralEntry.objects.get(key=song_key)
	except ObjectDoesNotExist:
		raise Http404()

	try:
		song = entry.song
		entry.delete()

		response = StreamingHttpResponse(
			(line for line in open(song.path, 'rb')))
		response['Content-Type'] = song.mime_type
		response['Content-Length'] = os.path.getsize(song.path)
		return response
	except FileNotFoundError:
		raise Http404('file does not exist')
