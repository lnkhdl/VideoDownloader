from downloader.video import Video
from pytube import Stream as PytubeStream
from pytube.cli import on_progress
import os, re

class Stream:
    def __init__(self, video: Video):
        self.video = video
        
        # Location where to save the file, e.g. C:\Users\Videos
        self.download_path = None
        
        # Filename, e.g. YouTubeRewind2020
        # By default, stream title is used, sanitized in set_download_filename
        self.download_filename = None
        
        # Filename with prefix and extension, e.g. Video_YouTubeRewind2020.mp4
        # By default, set_full_download_filename is used
        self.download_full_filename = None
        
        # Full location with a full filename, e.g. C:\Users\Videos\Video_YouTubeRewind2020.mp4
        self.download_file = None
        
        self.stream_id = None
        self.progress_callback = None
        self.set_progress_callback(on_progress)
        self.complete_callback = None
    
    def set_progress_callback(self, callback):
        self.progress_callback = callback
        
    def set_complete_callback(self, callback):
        self.complete_callback = callback
    
    def set_download_filename(self, original_title: str, max_length: int = 50) -> str:
        sanitized_title = "video"
        # Remove special characters, leaving only alphanumeric characters, spaces, and underscores
        sanitized_title = re.sub(r"[^\w\s]", "", original_title.strip())
        sanitized_title = sanitized_title.replace(" ", "_")
        sanitized_title = re.sub(r"_+", "_", sanitized_title)
        self.download_filename = sanitized_title[:max_length].lower()
    
    def set_download_full_filename(self, prefix: str, filename: str, extension: str) -> None:
        self.set_download_filename(filename)
        self.download_full_filename = prefix + self.download_filename + extension
    
    def set_download_file(self, path: str, full_filename: str) -> None:
        self.download_file = os.path.join(path, full_filename)
        
    def download_audio_only(self) -> None:
        self.stream_id = self.video.yt.streams.get_audio_only().itag
        self.download("audio_")
    
    def download_video_best_quality(self) -> None:
        self.stream_id = self.video.yt.streams.filter(progressive=True).order_by("resolution").desc().first().itag
        self.download("video_")
    
    def download(self, download_filename_prefix: str = "", download_filename_extension: str = ".mp4") -> None:
        print("Downloading started...")
        
        if self.progress_callback is not None:
            self.video.yt.register_on_progress_callback(self.progress_callback)
        
        if self.complete_callback is not None:
            self.video.yt.register_on_complete_callback(self.complete_callback)
        
        selected_stream = self.video.yt.streams.get_by_itag(self.stream_id)
        if selected_stream is not None:
            if self.download_full_filename is None:
                self.set_download_full_filename(download_filename_prefix, selected_stream.title, download_filename_extension)
            if self.download_file is None:
                self.set_download_file(self.download_path, self.download_full_filename)
            selected_stream.download(filename=self.download_file, skip_existing=False)
            print(f"Download completed. File saved at: {self.download_file}")
        else:
            print("The stream is not found.")
    
    def on_progress_gui_mode(self, stream: PytubeStream, chunk: bytes, bytes_remaining: int) -> None:
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        print(f"{int(percentage_of_completion)}% is done.")
