"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import sys
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from graphene_django.views import GraphQLView
from rest_framework import routers
from core.views import AlbumViewSet, ArtistViewSet, SongViewSet, FolderViewSet
from library_builder import parser
from server.schema import schema

if 'runserver' in sys.argv:
    parser.scan_directory('/Users/vados/Music')

router = routers.DefaultRouter()
router.register(r'albums', AlbumViewSet)
router.register(r'artists', ArtistViewSet)
router.register(r'songs', SongViewSet)
router.register(r'folders', FolderViewSet)

urlpatterns = [
    url(r'^jet/', include('jet.urls', 'jet')),
    path('admin/', admin.site.urls),
    path('graphql/', GraphQLView.as_view(graphiql=True, schema=schema)),
    path('media/', include('media.urls')),
    url(r'^', include(router.urls)),
]
