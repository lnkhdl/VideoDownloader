from flask import (
    Blueprint,
    render_template,
    g,
    request,
    jsonify,
    send_file,
)
from threading import Thread

bp = Blueprint("main", __name__)
download_queue = {}


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/process_url", methods=["POST"])
def process_url():
    data = request.get_json()
    url_entry = data.get("url")

    if not url_entry:
        return jsonify({"error": "No link provided"}), 400

    try:
        video = g.video

        if video.process_url(url_entry):
            details = {
                # more details can be added, like duration
                "title": video.yt.title,
            }
            streams = video.get_streams_combined()

            return jsonify(
                {
                    "success": True,
                    "details": details,
                    "streams": streams,
                }
            )
        else:
            return (
                jsonify(
                    {
                        "success": False,
                        "error": "Wrong link! Please correct it and try again.",
                    }
                ),
                400,
            )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# This sets a new download in the download_queue and starts the actual downloading from YouTube
@bp.route("/start_download", methods=["POST"])
def start_download():
    data = request.get_json()
    stream_id = data.get("stream_id")
    stream = g.stream
    stream.stream_id = stream_id

    queue_id = str(len(download_queue) + 1)
    download_queue[queue_id] = {"status": "in_progress"}

    thread = Thread(target=download_video_from_youtube, args=(stream, queue_id))
    thread.start()

    return jsonify({"queue_id": queue_id})


def download_video_from_youtube(stream, queue_id):
    stream.download()

    download_queue[queue_id]["status"] = "completed"
    download_queue[queue_id]["download_path"] = stream.download_file


# This is used to check if the download from YouTube is completed
@bp.route("/check_download_status/<queue_id>", methods=["GET"])
def check_download_status(queue_id):
    download = download_queue[queue_id]

    if download is None:
        return jsonify({"status": "error"}), 404
    if download["status"] == "completed":
        download_url = f"/download/{queue_id}"
        return jsonify({"status": "completed", "download_url": download_url})

    return jsonify({"status": "in_progress"})


# This is used to download the actual file from temp in the browser
@bp.route("/download/<queue_id>", methods=["GET"])
def download(queue_id):
    download = download_queue[queue_id]

    if download and download["status"] == "completed":
        return send_file(download["download_path"], as_attachment=True)

    return "File not ready yet", 404
