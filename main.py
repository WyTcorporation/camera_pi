import os

from PyQt6.QtWidgets import QApplication
import sys
from core.recorder import VideoRecorder
from core.audio import AudioRecorder
from gui.main_window import MainWindow
from core.webserver import WebControl
from core.gpio import GPIOController

if __name__ == '__main__':
    app = QApplication(sys.argv)

    video0 = VideoRecorder(device_index='/dev/video2', resolution=(3840, 2160), fps=30, save_dir="/mnt/nas")
    video2 = VideoRecorder(device_index='/dev/video2', resolution=(3840, 2160), fps=30, save_dir="/mnt/nas")
    # video0 = VideoRecorder(device_index='/dev/video0', resolution=(1920, 1080), fps=30)
    # video1 = VideoRecorder(device_index='/dev/video1', resolution=(3840, 2160), fps=30)
    # video2 = VideoRecorder(device_index='/dev/video2', resolution=(1280, 720), fps=30)

    audio = AudioRecorder()
    window = MainWindow(video0, video2, audio)

    video_recorders = {
        "cam0": video0,
        "cam2": video2
    }
    gpio = GPIOController(video_recorders, audio, gui_ref=window)
    web = WebControl(video_recorders, audio, gui_ref=window)
    web.start_background()
    window.show()

    # sys.exit(app.exec())
    try:
        sys.exit(app.exec())
    finally:
        gpio.stop()
