from downloader.video import Video
from pytube import Stream as PytubeStream
import os

class Stream:
    def __init__(self, video: Video):
        self.video = video
    
    def download(self, selected_stream_id: int, download_path: str) -> None:
        print("Downloading started...")
        self.video.yt.register_on_progress_callback(self.on_progress)
        streamYT = self.video.yt.streams.get_by_itag(selected_stream_id)
        if streamYT is not None:
            download_filename = os.path.join(download_path, "downloaded_video.mp4")
            streamYT.download(filename=download_filename)
            print(f"Download completed. File saved at: {download_filename}")
        else:
            print("Selected stream not found.")
    
    def on_progress(self, stream: PytubeStream, chunk: bytes, bytes_remaining: int) -> None:
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        percentage_of_completion = bytes_downloaded / total_size * 100
        print(f"{int(percentage_of_completion)}% is done.")