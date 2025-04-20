from fastapi import FastAPI
from fastapi.responses import JSONResponse
import threading

class WebControl:
    def __init__(self, video_recorder, audio_recorder):
        self.video = video_recorder
        self.audio = audio_recorder
        self.app = FastAPI()

        self.app.get("/start")(self.start_recording)
        self.app.get("/stop")(self.stop_recording)
        self.app.get("/status")(self.get_status)
        self.app.get("/last")(self.get_last_file)

    def start_background(self):
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        import uvicorn
        uvicorn.run(self.app, host="0.0.0.0", port=8080, log_level="info")

    def start_recording(self):
        if not self.video.recording:
            self.video.start()
            self.audio.start()
            return JSONResponse({"status": "recording started"})
        return JSONResponse({"status": "already recording"})

    def stop_recording(self):
        if self.video.recording:
            self.video.stop()
            self.audio.stop()
            return JSONResponse({"status": "recording stopped"})
        return JSONResponse({"status": "not recording"})

    def get_status(self):
        return JSONResponse({"recording": self.video.recording})

    def get_last_file(self):
        return JSONResponse({
            "video": self.video.get_file_path(),
            "audio": self.audio.get_file_path()
        })