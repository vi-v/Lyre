from django.contrib.auth.hashers import make_password
from django.db import migrations
import json

def create_default_artist(apps, schema_editor):
	Artist = apps.get_registered_model('core', 'Artist')
	artist = Artist()
	artist._id = 0
	artist.name = 'Unknown',
	artist.track_ids = json.dumps([])
	artist.num_tracks = 0
	artist.album_ids = json.dumps([])
	artist.num_albums = 0
	artist.save()


class Migration(migrations.Migration):
	dependencies = [
		('core', '0001_initial')
	]

	operations = [
		migrations.RunPython(create_default_artist),
	]
