from abc import ABC, abstractmethod
from downloader.video import Video
from downloader.stream import Stream

class Application(ABC):
    def __init__(self, video: Video, stream: Stream):
        super().__init__()
        
        self.video = video
        self.stream = stream
        
    @abstractmethod
    def start(self):
        pass