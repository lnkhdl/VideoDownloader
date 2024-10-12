from downloader.video import Video
from pytube import Stream as PytubeStream
import os, re

class Stream:
    def __init__(self, video: Video):
        self.video = video
        self.download_path = None
        self.stream_id = None
    
    def get_download_file_name(self, original_title: str, max_length: int = 50) -> str:
        # Remove special characters, leaving only alphanumeric characters, spaces, and underscores
        sanitized_title = re.sub(r"[^\w\s]", "", original_title.strip())
        sanitized_title = sanitized_title.replace(" ", "_")
        sanitized_title = re.sub(r"_+", "_", sanitized_title)
        return sanitized_title[:max_length].lower()
        
    def download_audio_only(self) -> None:
        self.stream_id = self.video.yt.streams.get_audio_only().itag
        self.download("audio_")
    
    def download_video_best_quality(self) -> None:
        self.stream_id = self.video.yt.streams.filter(progressive=True).order_by("resolution").desc().first().itag
        self.download("video_")
    
    def download(self, download_filename_prefix: str = "", download_filename_extension: str = ".mp4") -> None:
        print("Downloading started...")
        self.video.yt.register_on_progress_callback(self.on_progress)
        selected_stream = self.video.yt.streams.get_by_itag(self.stream_id)
        if selected_stream is not None:
            download_filename = os.path.join(self.download_path, download_filename_prefix + self.get_download_file_name(selected_stream.title) + download_filename_extension)
            selected_stream.download(filename=download_filename)
            print(f"Download completed. File saved at: {download_filename}")
        else:
            print("The stream is not found.")
    
    def on_progress(self, stream: PytubeStream, chunk: bytes, bytes_remaining: int) -> None:
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        print(f"{int(percentage_of_completion)}% is done.")