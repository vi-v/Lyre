import graphene
from core import schema
from core.models import Song, Artist, Album, Folder

class Query(schema.Query, graphene.ObjectType):
	pass

schema = graphene.Schema(query=Query)
