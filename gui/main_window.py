from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QTextEdit, QHBoxLayout, QGridLayout
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont, QImage, QPixmap
import cv2

class MainWindow(QWidget):
    def __init__(self, video0, video2, audio_recorder):
        super().__init__()
        self.setWindowTitle("Video Recorder GUI")
        self.setGeometry(100, 100, 600, 600)

        self.video0 = video0
        self.video2 = video2
        self.audio = audio_recorder

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frames)
        self.timer.start(1000 // int(max(self.video0.get_fps(), self.video2.get_fps())))

        self.init_ui()
        self.video0.open_camera()
        self.video2.open_camera()

    def init_ui(self):
        font = QFont("Arial", 14)

        self.status_label = QLabel("Статус: Зупинено")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(font)

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

    def start_recording(self):
        self.video0.start()
        self.video2.start()
        self.audio.start()
        self.status_label.setText("Статус: 🔴 Запис")
        self.log("▶️ Запис розпочато.")

    def stop_recording(self):
        self.video0.stop()
        self.video2.stop()
        self.audio.stop()
        self.status_label.setText("Статус: ⏹️ Зупинено")
        self.log("⏹️ Запис завершено.")

    def update_frames(self):
        frame0 = self.video0.write_frame()
        frame2 = self.video2.write_frame()

        if frame0 is not None:
            rgb0 = cv2.cvtColor(frame0, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb0.shape
            qimg0 = QImage(rgb0.tobytes(), w, h, ch * w, QImage.Format.Format_RGB888)
            self.preview_label0.setPixmap(QPixmap.fromImage(qimg0).scaled(
                self.preview_label0.width(),
                self.preview_label0.height(),
                Qt.AspectRatioMode.KeepAspectRatio))

        if frame2 is not None:
            rgb2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb2.shape
            qimg2 = QImage(rgb2.tobytes(), w, h, ch * w, QImage.Format.Format_RGB888)
            self.preview_label2.setPixmap(QPixmap.fromImage(qimg2).scaled(
                self.preview_label2.width(),
                self.preview_label2.height(),
                Qt.AspectRatioMode.KeepAspectRatio))

    def log(self, message):
        self.log_output.append(message)

    def closeEvent(self, event):
        self.video0.stop()
        self.video2.stop()
        self.audio.stop()
        super().closeEvent(event)

    def update_status_label(self, text):
        self.status_label.setText(f"Статус: {text}")
        self.log(f"{text}")
