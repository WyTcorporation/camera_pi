from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QTextEdit, QHBoxLayout, QGridLayout
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont, QImage, QPixmap

class MainWindow(QWidget):
    def __init__(self, video_recorder, audio_recorder):
        super().__init__()
        self.setWindowTitle("Video Recorder GUI")
        self.setGeometry(100, 100, 960, 600)

        self.video = video_recorder
        self.audio = audio_recorder

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.init_ui()

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

        self.preview_label = QLabel()
        self.preview_label.setFixedSize(640, 360)

        layout = QVBoxLayout()
        layout.addWidget(self.status_label)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        layout.addLayout(btn_layout)

        layout.addWidget(self.preview_label)
        layout.addWidget(self.log_output)
        self.setLayout(layout)

    def start_recording(self):
        self.video.start()
        self.audio.start()
        self.status_label.setText("Статус: 🔴 Запис")
        self.log("▶️ Запис розпочато.")
        self.timer.start(1000 // int(self.video.get_fps()))

    def stop_recording(self):
        self.timer.stop()
        self.video.stop()
        self.audio.stop()
        self.status_label.setText("Статус: ⏹️ Зупинено")
        self.log("⏹️ Запис завершено.")

    def update_frame(self):
        frame = self.video.write_frame()
        if frame is not None:
            rgb_frame = frame[..., ::-1]
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            qimg = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            pixmap = QPixmap.fromImage(qimg)
            self.preview_label.setPixmap(pixmap.scaled(
                self.preview_label.width(),
                self.preview_label.height(),
                Qt.AspectRatioMode.KeepAspectRatio))

    def log(self, message):
        self.log_output.append(message)

    def closeEvent(self, event):
        self.video.stop()
        self.audio.stop()
        super().closeEvent(event)