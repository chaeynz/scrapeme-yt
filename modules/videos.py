# pylint: disable=missing-docstring, line-too-long
import re
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4

ALLOWED_FILE_FORMATS = ['mp4']
DOWNLOAD_PATH = "/home/chaeynz/source/scrapeme-yt/content/yt/"




class VideoInfo:
    def __init__(self, file_name):
        self.metadata = self.extract_metadata(file_name)

    def extract_metadata(self, file_name):
        return {
            'publish_date': YouTube().publish_date,
            'title': YouTube().title,
            'channel_id': YouTube().channel_id,
            'channel_url': YouTube().channel_url,
            'video_id': YouTube().video_id,
            'length': YouTube().length,
            'available_format': ['mp4', 'mp3'],
            'playlists': [Playlist().playlist_id]
        }

class Videos:
    def __init__(self):
        self.pattern = r'([0-9A-Za-z_-]{11}).*'

    def __iter__(self):
        return iter([item for item in Path(DOWNLOAD_PATH).iterdir() if item.is_file() and re.search(self.pattern, item.name)])

    def __getitem__(self, index):
        files = [item for item in Path(DOWNLOAD_PATH).iterdir() if item.is_file() and (item.suffix in ALLOWED_FILE_FORMATS) and re.search(self.pattern, item.name)]
        return {
            'publish_date': '',
            'title': '',
            'channel_id': '',
            'channel_url': '',
            'video_id': '',
            'length': '',
            'available_format': ['mp4', 'mp3'],
            'playlists': [Playlist().playlist_id]
        }


    def __len__(self):
        return sum(1 for item in Path(DOWNLOAD_PATH).iterdir() if item.is_file() and re.search(self.pattern, item.name))
