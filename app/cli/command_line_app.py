from downloader.video import StreamType, Video
from downloader.stream import Stream
from helpers import clear_target_path
from app.base_app import Application


class CommandLineApp(Application):
    def __init__(self, video: Video, stream: Stream):
        super().__init__(video, stream)

    def start(self):
        self.ask_for_video_url()

    def ask_for_video_url(self, message=None):
        if message is not None:
            print(message)
        print("Please insert a YouTube video link: ")
        url_entry = input()
        self.validate_url(url_entry)

    def validate_url(self, url_entry):
        if self.video.process_url(url_entry):
            self.display_video_info()
            self.ask_if_download()
        else:
            self.ask_for_video_url("The link is not correct. Please try it again.")

    def display_video_info(self):
        print(f"\n{self.video.yt.title}")
        print(f"- Author: {self.video.yt.author}")
        print(f"- Views: {self.video.view_count}")
        print(f"- Duration: {self.video.duration}")

    def ask_if_download(self):
        print("\nWould you like to download the video? (Y/N)")
        selected = input().lower()
        if selected == "y" or selected == "yes":
            self.ask_which_stream_to_download()
        elif selected == "n" or selected == "no":
            self.ask_if_repeat()
        else:
            print("Invalid input. Please enter Y or N.")
            self.ask_if_download()

    def ask_which_stream_to_download(self):
        print("\nLoading the available streams. Please wait...")

        stream_ids = self.display_available_streams(StreamType.AUDIO)
        stream_ids.extend(self.display_available_streams(StreamType.VIDEO))

        print("\nWhich stream would you like to download? Please insert its ID.")
        selected_stream_id = input()
        try:
            if int(selected_stream_id) in stream_ids:
                target_path = self.ask_for_download_path()
                self.process_download(selected_stream_id, target_path)
            else:
                print(
                    "The selected ID is not correct. Please enter a valid numberic ID from the available streams."
                )
                self.ask_which_stream_to_download()
        except ValueError:
            print("Invalid input. Please enter a valid numberic ID.")
            self.ask_which_stream_to_download()

    def display_available_streams(self, stream_type: StreamType):
        streams = self.video.get_streams(stream_type)
        print(f"\nAvailable {stream_type.value} streams:")
        stream_ids = []
        for stream in streams:
            print(f"ID: {stream.itag}. Average bitrate: {stream.abr}.")
            stream_ids.append(stream.itag)
        return stream_ids

    def ask_for_download_path(self):
        print(
            "\nPlease specify a path where the file should be saved (or press Enter for the default location):"
        )
        selected_path = input()

        return clear_target_path(selected_path)

    def process_download(self, selected_stream_id, target_path):
        self.stream.stream_id = selected_stream_id
        self.stream.download_path = target_path
        self.stream.download()
        print("\nThe stream has been downloaded.")
        self.ask_if_repeat()

    def ask_if_repeat(self):
        print("Do you like to submit another YouTube video? (Y/N)")
        selected = input().lower()
        if selected == "y" or selected == "yes":
            self.ask_for_video_url()
        elif selected == "n" or selected == "no":
            print("Have a nice day!")
            exit()
        else:
            print("Invalid input. Please enter Y or N.")
            self.ask_if_repeat()
