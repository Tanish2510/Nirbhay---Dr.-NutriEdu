import os
from PyQt5 import QtMultimedia, QtCore
from PyQt5.QtMultimediaWidgets import QVideoWidget  # Import QVideoWidget
from PyQt5 import QtWidgets

class VideoHandler:
    def __init__(self, video_widget):
        """Initializes the video handler with a video widget."""
        if not isinstance(video_widget, QVideoWidget):  # Use QVideoWidget directly
            raise TypeError("video_widget must be an instance of QVideoWidget")

        self.video_widget = video_widget
        self.mediaPlayer = QtMultimedia.QMediaPlayer()
        self.mediaPlayer.setVideoOutput(self.video_widget)

    def load_video(self, video_path=r"C:\Users\hp\Downloads\Dr.Bharti.mp4"):
        """Loads and starts playing the video."""
        video_path = os.path.abspath(video_path)
        if not os.path.exists(video_path):
            print(f"Error: Video file not found at {video_path}")
            return False

        media = QtMultimedia.QMediaContent(QtCore.QUrl.fromLocalFile(video_path))
        self.mediaPlayer.setMedia(media)
        self.mediaPlayer.play()
        return True

    def stop_video_with_delay(self, delay=1):
        """Stops the video after a specified delay (in seconds)."""
        threading.Timer(delay, self.mediaPlayer.stop).start()

    def pause_video(self):
        """Pauses the video."""
        self.mediaPlayer.pause()

    def stop_video(self):
        """Stops the video."""
        self.mediaPlayer.stop()

    def set_volume(self, volume):
        """Sets the volume of the video (0-100)."""
        self.mediaPlayer.setVolume(volume)