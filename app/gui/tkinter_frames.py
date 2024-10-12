import customtkinter, tkinter, os
from PIL import Image
from downloader.video import StreamType
from app.helpers import clear_target_path
from pytubefix import Stream as PytubeStream
from typing import Optional


class Frame(customtkinter.CTkFrame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root

    def remove_current(self):
        if self.root.current_frame is not None:
            for widget in self.root.current_frame.winfo_children():
                widget.destroy()
            self.root.current_frame.grid_forget()


class UrlEntryFrame(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.remove_current()
        self.create_widgets()

    def create_widgets(self):
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.grid_columnconfigure(0, weight=1)

        # Header
        self.label = customtkinter.CTkLabel(
            self, width=700, text="Insert a YouTube link:", font=self.root.font_header
        )
        self.label.grid(row=0, column=0, padx=10, pady=(40))

        # Error when URL is incorrect
        self.error = customtkinter.CTkLabel(
            self,
            text="Wrong link! Please correct it and try again.",
            text_color="red",
            font=self.root.font,
        )

        # URL text input
        self.url_entry = customtkinter.CTkEntry(
            self,
            width=700,
            height=50,
            placeholder_text="https://www.youtube.com/watch?v=123abc",
        )
        self.url_entry.grid(row=2, column=0, padx=20, pady=40)

        # Navigation button
        self.button = customtkinter.CTkButton(
            self,
            width=self.root.button_width,
            height=self.root.button_height,
            text="Next",
            font=self.root.font,
            command=self.submit_link,
        )
        self.button.grid(row=3, column=0)

        # Allow submitting URL using Enter key
        self.url_entry.bind("<Return>", self.submit_link_by_enter_callback)

    def show_error(self):
        self.error.grid(row=1, column=0, padx=20)

    def hide_error(self):
        self.error.grid_forget()

    def submit_link(self):
        if self.root.video.process_url(self.url_entry.get()):
            self.hide_error()
            self.root.current_frame = VideoDetailFrame(self.root)
        else:
            self.show_error()

    def submit_link_by_enter_callback(self, event):
        self.submit_link()


class VideoDetailFrame(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.remove_current()
        self.create_widgets()

    def create_widgets(self):
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.grid_columnconfigure((0, 1), weight=1)

        # Header
        self.label = customtkinter.CTkLabel(
            self,
            text=self.root.video.yt.title,
            font=self.root.font_header,
            wraplength=600,
        )
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=(20, 40))

        # Left column - Image
        self.thumbnail = customtkinter.CTkImage(
            light_image=Image.open(self.root.video.thumbnail), size=(195, 110)
        )
        self.thumbnail_label = customtkinter.CTkLabel(
            self, image=self.thumbnail, text=""
        )
        self.thumbnail_label.grid(
            row=1, column=0, rowspan=3, padx=10, pady=5, stick="we"
        )

        # Right column - Video details
        self.author = customtkinter.CTkLabel(
            self,
            text="Author: " + self.root.video.yt.author,
            font=self.root.font,
            wraplength=200,
        )
        self.author.grid(row=1, column=1, padx=10, pady=5, stick="w")

        self.view_count = customtkinter.CTkLabel(
            self, text="Views: " + self.root.video.view_count, font=self.root.font
        )
        self.view_count.grid(row=2, column=1, padx=10, pady=5, stick="w")

        self.duration = customtkinter.CTkLabel(
            self, text="Duration: " + self.root.video.duration, font=self.root.font
        )
        self.duration.grid(row=3, column=1, padx=10, pady=5, stick="w")

        # Navigation buttons
        self.button_back = customtkinter.CTkButton(
            self,
            width=self.root.button_width,
            height=self.root.button_height,
            text="Back",
            font=self.root.font,
            command=self.back_to_url_entry,
        )
        self.button_back.grid(row=4, column=0, padx=10, pady=(40, 10), stick="e")
        self.button = customtkinter.CTkButton(
            self,
            width=self.root.button_width,
            height=self.root.button_height,
            text="Download options",
            font=self.root.font,
            command=self.go_to_download_options,
        )
        self.button.grid(row=4, column=1, padx=10, pady=(40, 10), stick="w")

    def go_to_download_options(self):
        self.root.current_frame = DownloadOptionsFrame(self.root)

    def back_to_url_entry(self):
        self.root.current_frame = UrlEntryFrame(self.root)


class DownloadOptionsFrame(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.remove_current()
        self.create_widgets()

    def create_widgets(self):
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        # self.grid_rowconfigure((0,1,2,3,4,5,6,7), weight=0)
        self.grid_columnconfigure((0, 1), weight=1)

        # Stream selection
        self.label1 = customtkinter.CTkLabel(
            self,
            text="Please select which stream to download:",
            font=self.root.font_header,
        )
        self.label1.grid(row=0, column=0, columnspan=2, pady=20, sticky="nsew")

        self.available_streams = self.get_streams()
        self.selected_stream = customtkinter.StringVar()
        self.combo_streams = customtkinter.CTkComboBox(
            self,
            height=self.root.combobox_height,
            values=list(self.available_streams.keys()),
            variable=self.selected_stream,
        )
        self.combo_streams.grid(row=1, column=0, columnspan=2)
        self.combo_streams.set(next(iter(self.available_streams.keys())))

        # Download path selection
        self.label2 = customtkinter.CTkLabel(
            self,
            text="Please select where to save the file:",
            font=self.root.font_header,
        )
        self.label2.grid(row=2, column=0, columnspan=2, pady=(40, 20), sticky="nsew")

        self.path_entry = customtkinter.CTkEntry(self, height=self.root.entry_height)
        self.path_entry.grid(row=3, column=0, columnspan=2, padx=10, sticky="ew")
        self.update_path_entry(os.getcwd())
        self.button_browse = customtkinter.CTkButton(
            self,
            width=self.root.button_width,
            height=self.root.button_height,
            text="Browse",
            font=self.root.font,
            command=self.process_path_browse,
        )
        self.button_browse.grid(
            row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ne"
        )

        # Navigation buttons
        self.button_back = customtkinter.CTkButton(
            self,
            width=self.root.button_width,
            height=self.root.button_height,
            text="Back",
            font=self.root.font,
            command=self.back_to_video_details,
        )
        self.button_back.grid(row=5, column=0, padx=10, pady=(40, 10), sticky="e")
        self.button = customtkinter.CTkButton(
            self,
            width=self.root.button_width,
            height=self.root.button_height,
            text="Download",
            font=self.root.font,
            command=self.start_download,
        )
        self.button.grid(row=5, column=1, padx=10, pady=(40, 10), sticky="w")

    def get_streams(self):
        streams_video = self.root.video.get_streams(StreamType.VIDEO)
        streams_audio = self.root.video.get_streams(StreamType.AUDIO)

        streams_dict = {}
        for streams in [streams_video, streams_audio]:
            for stream in streams:
                desc = (
                    f"Video {stream.abr}"
                    if stream in streams_video
                    else f"Audio {stream.abr}"
                )
                streams_dict[desc] = stream.itag

        return streams_dict

    def update_path_entry(self, text):
        self.path_entry.delete(0, tkinter.END)
        self.path_entry.insert(0, text)

    def process_path_browse(self):
        path = customtkinter.filedialog.askdirectory()
        self.update_path_entry(path)

    def start_download(self):
        self.root.stream.download_path = clear_target_path(self.path_entry.get())
        self.root.stream.stream_id = self.available_streams.get(
            self.combo_streams.get()
        )
        self.root.current_frame = DownloadFrame(self.root)

    def back_to_video_details(self):
        self.root.current_frame = VideoDetailFrame(self.root)


class DownloadFrame(Frame):
    def __init__(self, root):
        super().__init__(root)
        self.remove_current()
        self.create_widgets()

        self.root.stream.set_progress_callback(self.show_progress_bar)
        self.root.stream.set_complete_callback(self.show_widgets_after_download)
        self.root.stream.download()

    def create_widgets(self):
        self.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.grid_columnconfigure((0, 1), weight=1)

        self.label1 = customtkinter.CTkLabel(
            self, text="Download progress", font=self.root.font_header
        )
        self.label1.grid(row=0, column=0, columnspan=2, pady=20, sticky="nsew")

        self.percentage = customtkinter.CTkLabel(self, text="0 %", font=self.root.font)
        self.percentage.grid(row=1, column=0, columnspan=2, pady=10, sticky="nsew")

        self.progress = customtkinter.CTkProgressBar(self, height=30)
        self.progress.set(0)
        self.progress.grid(
            row=2, column=0, columnspan=2, padx=20, pady=10, sticky="nsew"
        )

    def show_progress_bar(
        self, stream: PytubeStream, chunk: bytes, bytes_remaining: int
    ) -> None:
        total_size = stream.filesize
        bytes_downloaded = total_size - bytes_remaining
        completion = bytes_downloaded / total_size
        self.percentage.configure(text=f"{int(completion*100)}%")
        self.percentage.update()
        self.progress.set(completion)

    def show_widgets_after_download(
        self, stream: PytubeStream, file_path: Optional[str]
    ):
        self.percentage.configure(text="The stream has been downloaded.")

        self.location = customtkinter.CTkLabel(
            self,
            text=self.root.stream.download_path,
            font=self.root.font,
            wraplength=600,
        )
        self.location.grid(row=3, column=0, columnspan=2, pady=(10, 5), sticky="nsew")
        self.location = customtkinter.CTkLabel(
            self,
            text=self.root.stream.download_full_filename,
            font=self.root.font,
            wraplength=600,
        )
        self.location.grid(row=4, column=0, columnspan=2, pady=(5, 20), sticky="nsew")

        self.button_back = customtkinter.CTkButton(
            self,
            width=self.root.button_width,
            height=self.root.button_height,
            text="Back",
            font=self.root.font,
            command=self.back_to_download_options,
        )
        self.button_back.grid(row=5, column=0, padx=10, pady=(40, 10), sticky="e")
        self.button = customtkinter.CTkButton(
            self,
            width=self.root.button_width,
            height=self.root.button_height,
            text="Submit new YT link",
            font=self.root.font,
            command=self.new_link,
        )
        self.button.grid(row=5, column=1, padx=10, pady=(40, 10), sticky="w")

    def new_link(self):
        self.root.current_frame = UrlEntryFrame(self.root)

    def back_to_download_options(self):
        self.root.current_frame = DownloadOptionsFrame(self.root)
