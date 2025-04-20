import subprocess
import os
from datetime import datetime

class AudioRecorder:
    def __init__(self, device="hw:0,0", rate=16000, channels=1, format="S16_LE", save_dir="/home/wytcorp/Projects/video_recorder/records"):
        self.device = device
        self.rate = rate
        self.channels = channels
        self.format = format
        self.save_dir = save_dir

        self.process = None
        self.current_file = None
        self.recording = False

    def start(self):
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder = os.path.join(self.save_dir, f"recording_{now}")
        os.makedirs(folder, exist_ok=True)

        filename = os.path.join(folder, "audio.wav")
        self.current_file = filename

        self.process = subprocess.Popen([
            "arecord",
            "-D", self.device,
            "-f", self.format,
            "-r", str(self.rate),
            "-c", str(self.channels),
            filename
        ])

        self.recording = True

    def stop(self):
        if self.process:
            self.process.terminate()
            self.process = None
            self.recording = False

    def get_file_path(self):
        return self.current_file