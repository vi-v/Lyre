from django.conf.urls import url
from django.urls import path
from media.views import stream_song

urlpatterns = [
	path('song/<int:song_id>/', stream_song, name='song_stream')
]
