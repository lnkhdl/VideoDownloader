from downloader.video import Video
from downloader.stream import Stream
from app.cli.command_line_app import CommandLineApp
from app.cli.arguments_app import ArgumentsApp
from app.gui.tkinter_app import TkinterApp
import sys


def main():
    gui_mode = True

    video = Video()
    stream = Stream(video)
    app = None

    # Check if command-line arguments are provided
    if len(sys.argv) > 1:
        app = ArgumentsApp(video, stream)

    # No command-line arguments, decide on the application mode
    else:
        if gui_mode:
            app = TkinterApp(video, stream)
        else:
            app = CommandLineApp(video, stream)

    app.start()


if __name__ == "__main__":
    main()
