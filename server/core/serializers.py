from core.models import Song, Album, Artist, Folder
from rest_framework import serializers


class CustomModelSerializer(serializers.HyperlinkedModelSerializer):
    extra_fields = []
    exclude_fields = []

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(
            CustomModelSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            expanded_fields += self.Meta.extra_fields

        if getattr(self.Meta, 'exclude_fields', None):
            expanded_fields = list(set(expanded_fields) ^
                                   set(self.Meta.exclude_fields))

        return expanded_fields


class AlbumSerializer(CustomModelSerializer):
    songs = serializers.SerializerMethodField('_get_songs')
    artist_name = serializers.SerializerMethodField('_get_artist_name')

    def _get_songs(self, obj):
        serializer = SongSerializer(
            obj.songs.all(),
            many=True,
            context={'request': None}
        )

        return serializer.data

    def _get_artist_name(self, obj):
        return obj.artist.name

    class Meta:
        model = Album
        fields = '__all__'
        extra_fields = ['_id', 'songs', 'artist_name']
    # fields = ('_id', 'name', 'artist', 'num_tracks', 'art', 'songs')


class ArtistSerializer(CustomModelSerializer):
    songs = serializers.SerializerMethodField('_get_songs')
    albums = serializers.SerializerMethodField('_get_albums')

    # print(len(albums))

    def _get_songs(self, obj):
        serializer = SongSerializer(
            obj.songs.all(),
            many=True,
            context={'request': None}
        )

        return serializer.data

    def _get_albums(self, obj):
        serializer = AlbumSerializer(
            obj.albums.all(),
            many=True,
            context={'request': None}
        )

        return serializer.data

    class Meta:
        model = Artist
        fields = '__all__'
        extra_fields = ['_id', 'songs', 'albums']
    # fields = ('_id', 'name', 'num_tracks', 'num_albums')


class SongSerializer(CustomModelSerializer):
    artist_name = serializers.SerializerMethodField('_get_artist_name')
    album_name = serializers.SerializerMethodField('_get_album_name')

    def _get_artist_name(self, obj):
        return obj.artist.name

    def _get_album_name(self, obj):
        return obj.album.name

    class Meta:
        model = Song
        fields = '__all__'
        extra_fields = ['_id', 'artist_name', 'album_name']
        exclude_fields = ['path']


class FolderSerializer(CustomModelSerializer):
    class Meta:
        model = Folder
        fields = '__all__'
        extra_fields = ['_id']
