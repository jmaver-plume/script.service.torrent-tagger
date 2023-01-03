import os
import re


class File:
    def __init__(self, filename, parent):
        self.filename = filename
        self.parent = parent

    def get_path(self):
        return f'{self.parent}/{self.filename}'

    def is_video_file(self):
        _, ext = os.path.splitext(self.filename)
        return bool(re.search(r'\.(mkv|mp4|mov|wmv|avi)', self.filename))
