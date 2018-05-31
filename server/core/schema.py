import graphene
from graphene_django.types import DjangoObjectType
from core.models import Album, Artist, Song, Folder

class SongType(DjangoObjectType):
	class Meta:
		model = Song
		
class ArtistType(DjangoObjectType):
	class Meta:
		model = Artist

class AlbumType(DjangoObjectType):
	class Meta:
		model = Album

class FolderType(DjangoObjectType):
	class Meta:
		model = Folder

class Query(object):
	song = graphene.Field(
		SongType,
		id=graphene.Int()
	)
	all_songs = graphene.List(SongType)

	artist = graphene.Field(
		ArtistType,
		id=graphene.Int()
	)
	all_artists = graphene.List(ArtistType)

	album = graphene.Field(
		AlbumType,
		id=graphene.Int()
	)
	all_albums = graphene.List(AlbumType)

	folder = graphene.Field(
		FolderType,
		id=graphene.Int()
	)
	all_folders = graphene.List(FolderType)

	def resolve_all_songs(self, info, **kwargs):
		return Song.objects.all()

	def resolve_song(self, info, **kwargs):
		id = kwargs.get('id')

		if id is not None:
			return Song.objects.get(pk=id)

		return None

	def resolve_all_artists(self, info, **kwargs):
		return Artist.objects.all()

	def resolve_artist(self, info, **kwargs):
		id = kwargs.get('id')

		if id is not None:
			return Artist.objects.get(pk=id)

		return None

	def resolve_all_albums(self, info, **kwargs):
		return Album.objects.all()

	def resolve_album(self, info, **kwargs):
		id = kwargs.get('id')

		if id is not None:
			return Album.objects.get(pk=id)

		return None

	def resolve_all_folders(self, info, **kwargs):
		return Folder.objects.all()

	def resolve_folder(self, info, **kwargs):
		id = kwargs.get('id')

		if id is not None:
			return Folder.objects.get(pk=id)

		return None
