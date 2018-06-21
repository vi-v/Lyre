import threading
import mimetypes
import os
import re
from flask import Flask, request, Response, abort, send_file
from media.models import EphemeralEntry


class Server(threading.Thread):
    def run(self):
        app = Flask(__name__)

        @app.after_request
        def after_request(response):
            response.headers.add('Accept-Ranges', 'bytes')
            return response

        # https://gist.github.com/lizhiwei/7885684
        @app.route('/song/<song_key>', methods=['GET'])
        def send_song(song_key):
            try:
                entry = EphemeralEntry.objects.get(key=song_key)
                song = entry.song

                try:
                    range_header = request.headers.get('Range', None)
                    if not range_header:
                        return send_file(song.path)

                    size = os.path.getsize(song.path)
                    byte1, byte2 = 0, None

                    m = re.search('(\d+)-(\d*)', range_header)
                    g = m.groups()

                    if g[0]:
                        byte1 = int(g[0])
                    if g[1]:
                        byte2 = int(g[1])

                    length = size - byte1
                    if byte2 is not None:
                        length = byte2 - byte1

                    with open(song.path, 'rb') as f:
                        f.seek(byte1)
                        data = f.read(length)

                    rv = Response(data,
                                  206,
                                  mimetype=mimetypes.guess_type(song.path)[0],
                                  direct_passthrough=True)
                    rv.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(byte1, byte1 + length - 1, size))

                    return rv
                except FileNotFoundError:
                    abort(404)
            except EphemeralEntry.DoesNotExist:
                abort(404)

        app.run(port=8001, host='0.0.0.0', debug=False, use_reloader=False)


def start():
    Server().start()
