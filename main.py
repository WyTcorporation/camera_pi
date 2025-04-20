from PyQt6.QtWidgets import QApplication
import sys
from core.recorder import VideoRecorder
from core.audio import AudioRecorder
from gui.main_window import MainWindow
from core.webserver import WebControl
from core.gpio import GPIOController


if __name__ == '__main__':
    app = QApplication(sys.argv)

    video = VideoRecorder()
    audio = AudioRecorder()
    window = MainWindow(video, audio)
    web = WebControl(video, audio)
    gpio = GPIOController(video, audio)

    web.start_background()
    window.show()

    try:
        sys.exit(app.exec())
    finally:
        gpio.stop()
