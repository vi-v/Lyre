from django.db import models
from core.models import Song

# Create your models here.

class EphemeralEntry(models.Model):
	song = models.ForeignKey(Song, on_delete=models.CASCADE)
	key = models.CharField(max_length=36)

	def __str__(self):
		return self.key + " - " + str(self.song)

	@staticmethod
	def clear_all():
		EphemeralEntry.objects.all().delete()
