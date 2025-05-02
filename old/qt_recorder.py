import sys
import subprocess
import shutil
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout,
    QLabel, QTextEdit, QHBoxLayout
)
from PyQt6.QtMultimediaWidgets import QCameraViewfinder
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont
from PyQt6.QtMultimedia import QCamera, QMediaDevices

class VideoRecorderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Raspberry Pi Video Recorder")
        self.setGeometry(100, 100, 800, 480)

        self.proc1 = None
        self.proc2 = None
        self.recording = False
        self.paused = False

        self.init_ui()
        self.update_disk_space()

        self.disk_timer = QTimer()
        self.disk_timer.timeout.connect(self.update_disk_space)
        self.disk_timer.start(10000)  # оновлення кожні 10 секунд

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

        self.preview1 = QCameraViewfinder()
        self.preview2 = QCameraViewfinder()
        self.preview1.setMinimumHeight(120)
        self.preview2.setMinimumHeight(120)

        available_cameras = QMediaDevices.videoInputs()
        if len(available_cameras) > 0:
            self.camera1 = QCamera(available_cameras[0])
            self.camera1.setViewfinder(self.preview1)
            self.camera1.start()
        if len(available_cameras) > 1:
            self.camera2 = QCamera(available_cameras[1])
            self.camera2.setViewfinder(self.preview2)
            self.camera2.start()

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)
        layout.addWidget(self.disk_label)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.pause_btn)
        btn_layout.addWidget(self.stop_btn)
        layout.addLayout(btn_layout)

        preview_layout = QHBoxLayout()
        preview_layout.addWidget(self.preview1)
        preview_layout.addWidget(self.preview2)
        layout.addLayout(preview_layout)

        layout.addWidget(self.log_output)
        self.setLayout(layout)

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

        from datetime import datetime
        date = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder = f"/home/wytcorp/Projects/video_recorder/records/recording_{date}"
        subprocess.run(["mkdir", "-p", folder])

        self.proc1 = subprocess.Popen([
            "ffmpeg",
            "-f", "v4l2", "-input_format", "mjpeg", "-framerate", "30",
            "-video_size", "1920x1080", "-i", "/dev/video0",

            "-f", "alsa", "-ac", "2", "-i", "hw:1,0",

            "-c:v", "libx264", "-preset", "ultrafast",
            "-c:a", "aac", "-b:a", "128k",
            f"{folder}/cam1_{date}.mp4"
        ])

        self.proc2 = subprocess.Popen([
            "ffmpeg", "-f", "v4l2", "-input_format", "mjpeg", "-framerate", "30",
            "-video_size", "1920x1080", "-i", "/dev/video2",
            "-c:v", "copy", f"{folder}/cam2_{date}.mkv"
        ])

        self.recording = True
        self.paused = False
        self.status_label.setText("Статус: 🔴 Запис")
        self.log("▶️ Запис розпочато.")

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoRecorderApp()
    window.show()
    sys.exit(app.exec())


