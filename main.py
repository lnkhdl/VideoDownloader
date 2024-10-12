from downloader.video import Video
from downloader.stream import Stream
from app.cli import CLI

def main():
    video = Video()
    stream = Stream(video)
    cli = CLI(video, stream)
    cli.ask_for_video_url()

if __name__ == "__main__":
    main()