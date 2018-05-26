from watchdog.events import FileSystemEventHandler


class FSHandler(FileSystemEventHandler):

    def on_moved(self, event):
        super(FSHandler, self).on_moved(event)

        what = 'directory' if event.is_directory else 'file'
        print("Moved %s: from %s to %s", what, event.src_path,
              event.dest_path)

    def on_created(self, event):
        super(FSHandler, self).on_created(event)

        what = 'directory' if event.is_directory else 'file'
        print("Created %s: %s", what, event.src_path)

    def on_deleted(self, event):
        super(FSHandler, self).on_deleted(event)

        what = 'directory' if event.is_directory else 'file'
        print("Deleted %s: %s", what, event.src_path)

    def on_modified(self, event):
        super(FSHandler, self).on_modified(event)

        what = 'directory' if event.is_directory else 'file'
        print("Modified %s: %s", what, event.src_path)
