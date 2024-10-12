from pytubefix import YouTube, exceptions, StreamQuery
from enum import Enum
import datetime
import urllib3
import os


class StreamType(Enum):
    AUDIO = "Audio"
    VIDEO = "Video"


class Video:
    def __init__(self):
        self.yt = None
        self._view_count = None
        self._duration = None
        self._thumbnail = None

    @property
    def view_count(self) -> str:
        self._view_count = "{:,d}".format(self.yt.views).replace(",", " ")
        return self._view_count

    @property
    def duration(self) -> str:
        self._duration = str(datetime.timedelta(seconds=self.yt.length))
        return self._duration

    @property
    def thumbnail(self) -> str:
        if self.download_thumbnail("thumbnail.png"):
            self._thumbnail = "thumbnail.png"
        else:
            self._thumbnail = "no_thumbnail.png"
        return self._thumbnail

    def process_url(self, url_entry: str) -> bool:
        try:
            self.yt = YouTube(url_entry)
            print(f"The link is correct: {url_entry}")
        except exceptions.VideoUnavailable as error:
            print(f"The link is correct, but the video is unavailable: {url_entry}")
            print(f"Video Unavailable error: {error}")
            return False
        except Exception as error:
            print(f"The link is wrong: {url_entry}")
            print(f"An exception occurred: {error}")
            return False

        return True

    def get_streams(self, stream_type: StreamType) -> StreamQuery:
        # PyTube bug related to Age restriction: https://github.com/pytube/pytube/issues/1712
        if stream_type == StreamType.AUDIO:
            return self.yt.streams.filter(only_audio=True, file_extension="mp4")
        elif stream_type == StreamType.VIDEO:
            return self.yt.streams.filter(progressive=True, file_extension="mp4")

    def download_thumbnail(self, filename: str) -> bool:
        try:
            with open(filename, "wb") as f:
                f.write(urllib3.request("GET", self.yt.thumbnail_url).data)
        except Exception as error:
            print("An exception occurred:", error)
            return False

        return True
