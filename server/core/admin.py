from django.contrib import admin
from .models import Artist, Album, Folder, Song

class SongInline(admin.StackedInline):
	model = Song

class AlbumInline(admin.StackedInline):
	model = Album

class ArtistAdmin(admin.ModelAdmin):
	inlines = [SongInline, AlbumInline]

class FolderAdmin(admin.ModelAdmin):
	inlines = [SongInline]

# Register your models here.
admin.site.register(Album)
admin.site.register(Song)

admin.site.register(Artist, ArtistAdmin)
admin.site.register(Folder, FolderAdmin)