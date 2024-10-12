import argparse
from app.helpers import get_target_path
from downloader.video import Video
from downloader.stream import Stream

class ArgumentsProcessor:
    def __init__(self):
        parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
            description="""
------------------------------------------------------------------------------------------------------------------------------

Application for downloading more YouTube videos at once by providing YouTube video URL/s in a text file, each on a new line.
To use CLI where more details about a YouTube video is provided as well as getting all the available streams to download, 
start the application without specifying any argument.

------------------------------------------------------------------------------------------------------------------------------
            """)
        parser.add_argument("-source", "-s", type=str, help="Full path and name of a txt file containing the YouTube video links, one per each line.")
        parser.add_argument("-type", "-t", type=str, choices=["video", "audio"], help="\"video\" means the best available stream containing also audio. \"audio\" means that only audio will be downloaded.")
        parser.add_argument("-directory", "-d", type=str, required=False, help="Path where to save the file. Optional. If not selected, the current working directory is used.")
        
        args = parser.parse_args()
        
        self.source_file = args.source
        self.target_path = get_target_path(args.directory)
        self.selected_type = args.type
        
        self.process_file()
        
    def process_file(self):
        try:
            with open(self.source_file, "r") as file:
                for line in file:
                    url = line.strip()
                    
                    video = Video()
                    if video.process_url(url):
                        stream = Stream(video)
                        if self.selected_type == "audio":
                            stream.download_audio_only(self.target_path)
                        else:
                            stream.download_video_best_quality(self.target_path)
                    else:
                        print(f"Wrong URL provided: {url}. Skipping this line.")
        except FileNotFoundError:
            print(f"The file is not found: {self.source_file}")
        except Exception as ex:
            print(ex)
