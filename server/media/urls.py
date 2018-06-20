from django.conf.urls import url
from django.urls import path
from media.views import stream_song, get_song_key

urlpatterns = [
    path('song/<int:song_id>/', get_song_key, name='song_ephemeral'),
    path('song/<slug:song_key>/', stream_song, name='song_stream'),
]
