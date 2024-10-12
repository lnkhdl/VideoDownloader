import argparse
from app.helpers import clear_target_path
from downloader.video import Video
from downloader.stream import Stream
from app.base_app import Application


class ArgumentsApp(Application):
    def __init__(self, video: Video, stream: Stream):
        super().__init__(video, stream)

        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="""
------------------------------------------------------------------------------------------------------------------------------

Application for downloading more YouTube videos at once by providing YouTube video URL/s in a text file, each on a new line.
To use CLI where more details about a YouTube video is provided as well as getting all the available streams to download, 
start the application without specifying any argument.

------------------------------------------------------------------------------------------------------------------------------
            """,
        )
        parser.add_argument(
            "-source",
            "-s",
            type=str,
            help="Full path and name of a txt file containing the YouTube video links, one per each line.",
        )
        parser.add_argument(
            "-type",
            "-t",
            type=str,
            choices=["video", "audio"],
            help='"video" means the best available stream containing also audio. "audio" means that only audio will be downloaded.',
        )
        parser.add_argument(
            "-directory",
            "-d",
            type=str,
            required=False,
            help="Path where to save the file. Optional. If not selected, the current working directory is used.",
        )

        args = parser.parse_args()

        self.source_file: str = args.source
        self.target_path: str = clear_target_path(args.directory)
        self.stream.download_path = self.target_path
        self.selected_type: str = args.type

    def start(self):
        try:
            with open(self.source_file, "r") as file:
                for line in file:
                    url = line.strip()

                    if self.video.process_url(url):
                        if self.selected_type.lower() == "audio":
                            self.stream.download_audio_only()
                        else:
                            self.stream.download_video_best_quality()
                    else:
                        print(f"Wrong URL provided: {url}. Skipping this line.")
        except FileNotFoundError:
            print(f"The file is not found: {self.source_file}")
        except Exception as ex:
            print(ex)
