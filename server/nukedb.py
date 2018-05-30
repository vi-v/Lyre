from core.models import Song, Album, Folder

Song.objects.all().delete()
Album.objects.all().delete()
Folder.objects.all().delete()

