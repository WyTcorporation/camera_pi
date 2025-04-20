import sys
import subprocess
import shutil
import cv2
import threading
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QGridLayout
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont, QImage, QPixmap

class VideoRecorderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Raspberry Pi Video Recorder")
        self.setGeometry(100, 100, 960, 600)

        self.proc1 = None
        self.proc2 = None
        self.recording = False
        self.paused = False

        self.cam0 = cv2.VideoCapture(0)
        self.cam2 = cv2.VideoCapture(2)

        self.init_ui()
        self.update_disk_space()

        self.timer_preview = QTimer()
        self.timer_preview.timeout.connect(self.update_preview)
        self.timer_preview.start(30)

        self.disk_timer = QTimer()
        self.disk_timer.timeout.connect(self.update_disk_space)
        self.disk_timer.start(10000)

    def init_ui(self):
        font = QFont("Arial", 14)

        self.status_label = QLabel("Статус: Зупинено")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(font)

        self.disk_label = QLabel("Вільно: ?")
        self.disk_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.disk_label.setFont(QFont("Arial", 12))

        self.start_btn = QPushButton("▶️ Старт")
        self.pause_btn = QPushButton("⏸️ Пауза")
        self.stop_btn = QPushButton("⏹️ Стоп")

        self.start_btn.setFont(font)
        self.pause_btn.setFont(font)
        self.stop_btn.setFont(font)

        self.start_btn.clicked.connect(self.start_recording)
        self.pause_btn.clicked.connect(self.toggle_pause)
        self.stop_btn.clicked.connect(self.stop_recording)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.setFont(QFont("Courier", 10))

        self.preview_label0 = QLabel()
        self.preview_label2 = QLabel()
        self.preview_label0.setFixedSize(400, 225)
        self.preview_label2.setFixedSize(400, 225)

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.disk_label)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.pause_btn)
        btn_layout.addWidget(self.stop_btn)
        layout.addLayout(btn_layout)

        grid = QGridLayout()
        grid.addWidget(QLabel("Камера 0"), 0, 0)
        grid.addWidget(QLabel("Камера 2"), 0, 1)
        grid.addWidget(self.preview_label0, 1, 0)
        grid.addWidget(self.preview_label2, 1, 1)
        layout.addLayout(grid)

        layout.addWidget(self.log_output)
        self.setLayout(layout)

    def update_preview(self):
        self.show_camera_frame(self.cam0, self.preview_label0)
        self.show_camera_frame(self.cam2, self.preview_label2)

    def show_camera_frame(self, cam, label):
        ret, frame = cam.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qimg = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
            label.setPixmap(pixmap.scaled(label.width(), label.height(), Qt.AspectRatioMode.KeepAspectRatio))

    def log(self, message):
        self.log_output.append(message)

    def update_disk_space(self):
        total, used, free = shutil.disk_usage("/home/wytcorp/Projects/video_recorder/records/")
        free_gb = free // (2**30)
        self.disk_label.setText(f"Вільно: {free_gb} ГБ")

    def start_recording(self):
        if self.recording:
            self.log("🔁 Вже йде запис.")
            return

        date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder = f"/home/wytcorp/Projects/video_recorder/records/recording_{date}"
        subprocess.run(["mkdir", "-p", folder])

        self.timer_preview.stop()
        self.cam0.release()
        self.cam2.release()

        self.proc1 = subprocess.Popen([
            "ffmpeg",
            "-f", "v4l2", "-input_format", "mjpeg", "-framerate", "30",
            "-video_size", "1920x1080", "-i", "/dev/video0",

            "-f", "alsa", "-ac", "2", "-i", "hw:1,0",

            "-c:v", "libx264", "-preset", "ultrafast",
            "-c:a", "aac", "-b:a", "128k",
            f"{folder}/cam1_{date}.mp4"
        ], stderr=subprocess.PIPE, stdout=subprocess.DEVNULL)

        self.proc2 = subprocess.Popen([
            "ffmpeg", "-f", "v4l2", "-input_format", "mjpeg", "-framerate", "30",
            "-video_size", "1920x1080", "-i", "/dev/video2",
            "-c:v", "libx264", "-preset", "ultrafast", f"{folder}/cam2_{date}.mkv"
        ], stderr=subprocess.PIPE, stdout=subprocess.DEVNULL)

        self.recording = True
        self.paused = False
        self.status_label.setText("Статус: 🔴 Запис")
        self.log("▶️ Запис розпочато.")

        self.log("🔍 FFmpeg log:")
        self.log(self.proc1.stderr.read().decode('utf-8'))

    def toggle_pause(self):
        if not self.recording:
            return

        if self.paused:
            self.proc1.send_signal(subprocess.signal.SIGCONT)
            self.proc2.send_signal(subprocess.signal.SIGCONT)
            self.status_label.setText("Статус: 🔴 Запис")
            self.log("🔄 Запис продовжено.")
            self.paused = False
        else:
            self.proc1.send_signal(subprocess.signal.SIGSTOP)
            self.proc2.send_signal(subprocess.signal.SIGSTOP)
            self.status_label.setText("Статус: ⏸️ На паузі")
            self.log("⏸️ Запис призупинено.")
            self.paused = True

    def stop_recording(self):
        if self.recording:
            self.proc1.terminate()
            self.proc2.terminate()
            self.proc1 = None
            self.proc2 = None
            self.recording = False
            self.paused = False
            self.status_label.setText("Статус: ⏹️ Зупинено")
            self.log("⏹️ Запис завершено.")

            self.cam0 = cv2.VideoCapture(0)
            self.cam2 = cv2.VideoCapture(2)
            self.timer_preview.start(30)

    def closeEvent(self, event):
        self.cam0.release()
        self.cam2.release()
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoRecorderApp()
    window.show()
    sys.exit(app.exec())
