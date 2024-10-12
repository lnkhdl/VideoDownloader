from downloader.video import Video
from downloader.stream import Stream
from app.cli.command_line_app import CommandLineApp
from app.cli.arguments_app import ArgumentsApp
from app.gui.tkinter_app import TkinterApp
import sys, customtkinter

def main():
    gui: bool = True
    
    video = Video()
    stream = Stream(video)
    processor = None
    
    # arguments provided
    if len(sys.argv) > 1:
        processor = ArgumentsApp(video, stream)
        processor.process_file()
    
    # only main file is called
    else:
        if gui:
            processor = TkinterApp(video, stream)
            # Modes: system, light, dart
            customtkinter.set_appearance_mode("dark")

            # Themes: blue, dark-blue, green
            customtkinter.set_default_color_theme("blue")

            processor.mainloop()
        else:
            processor = CommandLineApp(video, stream)
            processor.ask_for_video_url()

if __name__ == "__main__":
    main()