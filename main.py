from downloader.video import Video
from downloader.stream import Stream
from app.cli.command_line_app import CommandLineApp
from app.cli.arguments_app import ArgumentsApp
from app.gui.tkinter_app import TkinterApp
from app.web.web_app import WebApp
from helpers import remove_old_tmp_files
import sys


def main():
    """
    Set Mode:
           arg ... multiple command-line arguments is used

           cmd ... command line mode is started
           gui ... Tkinter app is started
           web ... Flask web is started
    """

    if len(sys.argv) > 1:
        mode = "arg"
    else:
        mode = "web"

    video = Video()
    stream = Stream(video, mode)
    app = None

    # If command-line arguments are provided, multiple download is triggered
    if len(sys.argv) > 1:
        app = ArgumentsApp(video, stream)

    # If no command-line arguments are provided, decide which application mode to start
    else:
        if mode == "cmd":
            app = CommandLineApp(video, stream)
        elif mode == "gui":
            app = TkinterApp(video, stream)
        elif mode == "web":
            remove_old_tmp_files()
            app = WebApp(video, stream)
        else:
            print("Wrong mode selected.")
            exit()

    app.start()


if __name__ == "__main__":
    main()
