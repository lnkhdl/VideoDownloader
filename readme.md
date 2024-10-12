# Video Downloader

This project is a Python-based Video Downloader with multiple user interfaces. **It was created purely for learning purposes and is not production-ready.** The project consists of several modes to experiment with different Python tools and libraries for user interaction.

## Disclaimer

This project is for educational purposes only. Downloading YouTube videos may violate YouTube's Terms of Service if done without permission from the content creator or for purposes other than personal use. I do not condone or encourage the illegal downloading or distribution of copyrighted content. Please ensure that you have the necessary rights or permissions before downloading any videos.


## Project Overview

The core functionality of the project is to download videos. It offers multiple modes of user interaction. Each mode provides a similar core functionality but differs in the way the user interacts with the application.

### Notes
- This is my first Python project. It was developed to explore various Python programming concepts.
- The project was primarily developed for learning purposes, and while it functions as intended, it hasn't been fully optimized for production use. It does not handle concurrency (threading) and other advanced production features. It includes basic exception handling but there may be cases or situations that haven't been fully accounted for, such as retrying failed downloads or handling network issues robustly.
- The project was developed and tested on Windows only. It may require adjustments to work on other operating systems.
- Git commits were added retrospectively after the changes were made.
  
### Modes of Operation

#### 1. Argument-Based Application
- In this mode, the user can run the script with command-line arguments and downlod more files by one command.

Example usage:
```bash
python main.py -s C:\my_files\yt_links.txt -t audio -d C:\my_files\downloads\audio
```

#### 2. Command-Line Interface (CLI)
- The CLI mode allows users to run the program directly from the terminal.
- In main.py, set the mode to `cmd`.
  
#### 3. Graphical User Interface (Tkinter)
- The GUI version of the downloader uses Tkinter, a built-in Python library for creating desktop applications.
- Users can input the video URL in a window-based interface.
- In main.py, set the mode to `gui`.

#### 4. Graphical User Interface (Tkinter)
- The Flask-based web version allows the downloader to run as a web app.
- Users can input the URL in a web form and download the video through the browser.
- In main.py, set the mode to `web`.
- Open http://127.0.0.1:5000/ in your browser.

### Usage
```bash
cd path\to\the\project
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### Screenshots
Screenshots are available in the `_screenshots` folder.

![GUI](./_screenshots/gui01.png "GUI]")

![WEB](./_screenshots/web01.png "WEB]")