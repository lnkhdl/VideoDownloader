from downloader.video import Video
from downloader.stream import Stream
from app.cli import CLI
from app.arguments_processor import ArgumentsProcessor
import sys

def main():
    video = Video()
    stream = Stream(video)
    cli = CLI(video, stream)
    cli.ask_for_video_url()   

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ArgumentsProcessor()
    else:
        main()