from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import threading
import os

class WebControl:
    def __init__(self, video_recorders, audio_recorder, gui_ref=None):
        self.videos = video_recorders
        self.audio = audio_recorder
        self.gui = gui_ref
        self.app = FastAPI()

        # HTML шаблони та статика
        root_path = os.path.dirname(os.path.abspath(__file__))
        self.templates = Jinja2Templates(directory=os.path.join(root_path, "../templates"))
        self.app.mount("/static", StaticFiles(directory=os.path.join(root_path, "../static")), name="static")

        # Роутинг
        self.app.get("/", response_class=HTMLResponse)(self.index)
        self.app.get("/start")(self.start_recording)
        self.app.get("/stop")(self.stop_recording)
        self.app.get("/status")(self.get_status)
        self.app.get("/last")(self.get_last_file)

    def start_background(self):
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        import uvicorn
        uvicorn.run(self.app, host="0.0.0.0", port=8080, log_level="info")

    async def index(self, request: Request):
        return self.templates.TemplateResponse("index.html", {"request": request})

    async def start_recording(self, request: Request = None):
        started = False
        if self.gui:
            self.gui.update_status_label("🔴 Запис з веб-інтерфейсу")

        for video in self.videos.values():
            if not video.recording:
                video.start()
                started = True

        if not self.audio.recording:
            self.audio.start()
            started = True

        return JSONResponse({"status": "recording started" if started else "already recording"})

    async def stop_recording(self, request: Request = None):
        stopped = False
        if self.gui:
            self.gui.update_status_label("⏹️ Зупинено через веб")

        for video in self.videos.values():
            if video.recording:
                video.stop()
                stopped = True

        if self.audio.recording:
            self.audio.stop()
            stopped = True

        return JSONResponse({"status": "recording stopped" if stopped else "already stopped"})

    async def get_status(self, request: Request = None):
        status = {name: video.recording for name, video in self.videos.items()}
        status["audio"] = self.audio.recording
        return JSONResponse(status)

    async def get_last_file(self, request: Request = None):
        files = {name: video.get_file_path() for name, video in self.videos.items()}
        files["audio"] = self.audio.get_file_path()
        return JSONResponse(files)
