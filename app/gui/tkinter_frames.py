import customtkinter
from PIL import Image

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
        self.grid(row=0, column=0, padx=20, pady=20)

        self.label = customtkinter.CTkLabel(self, width=700, text="Insert a YouTube link:", font=self.root.font_header)
        self.label.grid(row=0, column=0, padx=10, pady=(20, 10))

        self.error = customtkinter.CTkLabel(self, text="Wrong link! Please correct it and try again.", text_color="red")
        
        self.url_entry = customtkinter.CTkEntry(self, width=700, height=50, placeholder_text="https://www.youtube.com/watch?v=123abc")
        self.url_entry.grid(row=2, column=0, padx=20, pady=(20, 10))

        self.button = customtkinter.CTkButton(self, width=self.root.button_width, height=self.root.button_height, text="Next", font=self.root.font, command=self.submit_link)
        self.button.grid(row=3, column=0, pady=30)

        # Allow submitting URL using Enter key
        self.url_entry.bind("<Return>", self.submit_link_by_enter_callback)
    
    def show_error(self):
        self.error.grid(row=1, column=0, padx=20, pady=(20, 10))
    
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
        self.grid(row=0, column=0, padx=20, pady=20)

        self.label = customtkinter.CTkLabel(self, width=700, text=self.root.video.yt.title, font=self.root.font_header, wraplength=500)
        self.label.grid(row=0, column=0, columnspan=2, padx=10, pady=30)

        self.thumbnail = customtkinter.CTkImage(light_image=Image.open(self.root.video.thumbnail), size=(170, 96))
        self.thumbnail_label = customtkinter.CTkLabel(self, image=self.thumbnail, text="")
        self.thumbnail_label.grid(row=1, column=0, rowspan=3, padx=10, pady=5)

        self.author = customtkinter.CTkLabel(self, text="Author: " + self.root.video.yt.author, font=self.root.font, wraplength=300)
        self.author.grid(row=1, column=1, padx=10, pady=5, stick="w")

        self.view_count = customtkinter.CTkLabel(self, text="Views: " + self.root.video.view_count, font=self.root.font)
        self.view_count.grid(row=2, column=1, padx=10, pady=5, stick="w")

        self.duration = customtkinter.CTkLabel(self, text="Duration: " + self.root.video.duration, font=self.root.font)
        self.duration.grid(row=3, column=1, padx=10, pady=5, stick="w")

        self.button_back = customtkinter.CTkButton(self, width=self.root.button_width, height=self.root.button_height, text="Back", font=self.root.font, command=self.back_to_url_entry)
        self.button_back.grid(row=4, column=0, padx=10, pady=30, stick="e")
        self.button = customtkinter.CTkButton(self, width=self.root.button_width, height=self.root.button_height, text="Download", font=self.root.font, command= lambda: self.download_video)
        self.button.grid(row=4, column=1, padx=10, pady=30, stick="w")
    
    def download_video(self):
        print("Video download clicked.")

    def back_to_url_entry(self):
        self.root.current_frame = UrlEntryFrame(self.root)
