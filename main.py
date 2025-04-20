from core.recorder import VideoRecorder
from core.audio import AudioRecorder
from PyQt6.QtWidgets import QApplication
from gui.main_window import MainWindow
import sys
from core.webserver import WebControl
from core.gpio import GPIOController

class VideoApp:
    def __init__(self):
        self.video = VideoRecorder()
        self.audio = AudioRecorder()
        self.gui = MainWindow(self.video, self.audio)
        self.web = WebControl(self.video, self.audio)
        self.gpio = GPIOController(self.video, self.audio)
        self.web.start_background()

    def run(self):
        app = QApplication(sys.argv)
        self.gui.show()
        sys.exit(app.exec())

if __name__ == '__main__':
    VideoApp().run()
