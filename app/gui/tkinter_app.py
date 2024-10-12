from downloader.video import Video
from downloader.stream import Stream
from app.helpers import get_target_path
from app.gui.tkinter_frames import UrlEntryFrame, VideoDetailFrame
from app.base_app import Application

import customtkinter

available_frames = {
    "UrlEntryFrame": UrlEntryFrame,
    "VideoDetailFrame": VideoDetailFrame
}


class TkinterApp(Application, customtkinter.CTk):
    def __init__(self, video: Video, stream: Stream):
        super().__init__(video, stream)
        
        self.current_frame = None
        
        # FONTS
        self.font_header = customtkinter.CTkFont("Arial", 20, "bold")
        self.font = customtkinter.CTkFont("Arial", 16)
        self.font_small = customtkinter.CTkFont("Arial", 10)

        # BUTTONS
        self.button_width = 80
        self.button_height = 30

        # WINDOW
        self.geometry("800x500")
        self.title("YouTube Downloader")
        self.resizable(0, 0)

        # GRID
        self.grid_rowconfigure(0, weight=1)

        # FIRST FRAME
        self.current_frame = UrlEntryFrame(self)

        # STATIC FOOTER
        self.footer = customtkinter.CTkLabel(self, text="2024 @ LNKHDL", text_color="gray", font=self.font_small)
        self.footer.grid(row=1, column=0, padx=40, pady=(0,10), sticky="e")
    
    def start(self):
        # Modes: system, light, dart
        customtkinter.set_appearance_mode("dark")

        # Themes: blue, dark-blue, green
        customtkinter.set_default_color_theme("blue")

        self.mainloop()
