from downloader.video import Video
from downloader.stream import Stream
from app.base_app import Application
from flask import Flask, g
from app.web.routes import bp


class WebApp(Application):
    def __init__(self, video: Video, stream: Stream):
        super().__init__(video, stream)
        self.app = None

    def create_app(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(bp)

        # Attach the Video and Stream objects to the g object
        # By using Flask’s g object and before_request, objects can be passed into the Flask request context
        @self.app.before_request
        def load_video_stream():
            g.video = self.video
            g.stream = self.stream

    def start(self):
        self.create_app()
        self.app.run(debug=True, host="0.0.0.0", port=5000)
