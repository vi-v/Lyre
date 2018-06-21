import subprocess
import os
import click
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
application = get_wsgi_application()


@click.group()
def cli():
    """Welcome to lyre!
        For further information about commands, use the --help flag.
        Ex: lyre --help
    """


@click.command()
@click.option('--port', default='8000', help="Port to run the server on.")
def run(port):
    run_command = 'gunicorn -w 4 -b :{0} server.wsgi'.format(port)
    subprocess.call(run_command.split())


@click.command()
@click.argument('path', nargs=1)
def build(path):
    from media.models import Song
    from library_builder import parser

    parser.scan_directory(path)


@click.command()
def clear():
    from core.models import Song, Album, Folder

    click.echo('Clearing library database...')

    num_songs = Song.objects.all().count()
    num_albums = Album.objects.all().count()
    num_folders = Folder.objects.all().count()

    Song.objects.all().delete()
    Album.objects.all().delete()
    Folder.objects.all().delete()

    click.echo('Deleted {0} songs, {1} albums, and {2} folders'.format(
        num_songs, num_albums, num_folders))


cli.add_command(run)
cli.add_command(build)
cli.add_command(clear)

if __name__ == '__main__':
    cli()
