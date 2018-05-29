from django.contrib import admin
from .models import Artist, Album, Folder, Song 

# Register your models here.
admin.site.register(Album)
admin.site.register(Artist)
admin.site.register(Folder)
admin.site.register(Song)
