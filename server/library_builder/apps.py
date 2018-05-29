from django.apps import AppConfig
from library_builder import parser

class LibraryBuilderConfig(AppConfig):
    name = 'library_builder'

    def ready(self):
        pass
        # parser.scan_directory('~/Music')
