import cv2
import os
from datetime import datetime

class VideoRecorder:
    def __init__(self, device_index=0, resolution=(640, 480), fps=30, save_dir="/home/wytcorp/Projects/video_recorder/records"):
        self.device_index = device_index
        self.resolution = resolution
        self.fps = fps
        self.save_dir = save_dir

        self.cam = None
        self.writer = None
        self.recording = False
        self.current_file = None

    def open_camera(self):
        self.cam = cv2.VideoCapture(self.device_index)
        self.cam.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
        self.cam.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
        self.cam.set(cv2.CAP_PROP_FPS, self.fps)

    def start(self):
        if self.recording:
            return

        if not self.cam or not self.cam.isOpened():
            self.open_camera()

        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder = os.path.join(self.save_dir, f"recording_{now}")
        os.makedirs(folder, exist_ok=True)

        filename = os.path.join(folder, f"cam{self.device_index}.mp4")
        self.current_file = filename
        self.writer = cv2.VideoWriter(
            filename,
            cv2.VideoWriter_fourcc(*'mp4v'),
            self.fps,
            self.resolution
        )
        self.recording = True

    def write_frame(self):
        if self.cam is None:
            return None

        ret, frame = self.cam.read()
        if not ret:
            return None

        if self.recording and self.writer:
            self.writer.write(frame)

        return frame

    def stop(self):
        if self.writer:
            self.writer.release()
        if self.cam:
            self.cam.release()
        self.recording = False

    def get_resolution(self):
        return self.resolution

    def get_fps(self):
        return self.fps

    def get_file_path(self):
        return self.current_file
