import sys
import cv2
import shutil
import subprocess
from datetime import datetime
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QTextEdit, QHBoxLayout, QGridLayout
)
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont, QImage, QPixmap

class VideoRecorderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Recorder FINAL")
        self.setGeometry(100, 100, 960, 600)

        self.cam0 = cv2.VideoCapture(0)
        self.cam2 = cv2.VideoCapture(2)

        # Read true frame sizes and FPS
        self.w0 = int(self.cam0.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.h0 = int(self.cam0.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps0 = self.cam0.get(cv2.CAP_PROP_FPS)
        # if self.fps0 <= 0: self.fps0 = 30

        self.w2 = int(self.cam2.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.h2 = int(self.cam2.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps2 = self.cam2.get(cv2.CAP_PROP_FPS)
        # if self.fps2 <= 0: self.fps2 = 30

        self.fps0 = 15
        self.fps2 = 15


        self.writer0 = None
        self.writer2 = None
        self.audio_proc = None

        self.recording = False

        self.init_ui()
        self.update_disk_space()

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_preview)


        # self.timer.start(1000 // int(max(self.fps0, self.fps2)))
        self.timer.start(1000 // 15)

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
        self.stop_btn = QPushButton("⏹️ Стоп")

        self.start_btn.setFont(font)
        self.stop_btn.setFont(font)

        self.start_btn.clicked.connect(self.start_recording)
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
        ret0, frame0 = self.cam0.read()
        ret2, frame2 = self.cam2.read()

        if ret0:
            self.show_frame(frame0, self.preview_label0)
            if self.recording:
                self.writer0.write(frame0)

        if ret2:
            self.show_frame(frame2, self.preview_label2)
            if self.recording:
                self.writer2.write(frame2)

    def show_frame(self, frame, label):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_frame.shape
        bytes_per_line = ch * w
        qimg = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
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

        self.writer0 = cv2.VideoWriter(
            f"{folder}/cam0.mp4", cv2.VideoWriter_fourcc(*'mp4v'), self.fps0, (self.w0, self.h0))
        self.writer2 = cv2.VideoWriter(
            f"{folder}/cam2.mp4", cv2.VideoWriter_fourcc(*'mp4v'), self.fps2, (self.w2, self.h2))

        self.audio_proc = subprocess.Popen([
            "ffmpeg",
            "-f", "alsa",
            "-ac", "1",  # 1 канал
            "-ar", "16000",  # 16000 Гц (НЕ 44100!)
            "-sample_fmt", "s16",  # формат S16_LE
            "-i", "hw:0,0",
            "-c:a", "aac",
            "-b:a", "64k",
            f"{folder}/audio.wav"
        ])

        self.recording = True
        self.status_label.setText("Статус: 🔴 Запис")
        self.log("▶️ Запис розпочато.")

    def stop_recording(self):
        if not self.recording:
            return

        self.recording = False
        self.writer0.release()
        self.writer2.release()
        if self.audio_proc:
            self.audio_proc.terminate()

        self.status_label.setText("Статус: ⏹️ Зупинено")
        self.log("⏹️ Запис завершено.")

    def closeEvent(self, event):
        self.cam0.release()
        self.cam2.release()
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = VideoRecorderApp()
    window.show()
    sys.exit(app.exec())
