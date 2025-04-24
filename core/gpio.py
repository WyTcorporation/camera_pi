from gpiozero import Button, RGBLED
import threading
import time

class GPIOController:
    def __init__(self, video_recorders, audio_recorder,
                 start_pin=17, stop_pin=22,  gui_ref=None,led_pins=(5, 6, 13)):
        self.videos = video_recorders
        self.audio = audio_recorder
        self.gui = gui_ref

        self.btn_start = Button(start_pin, pull_up=True, bounce_time=0.1)
        self.btn_stop = Button(stop_pin, pull_up=True, bounce_time=0.1)
        self.rgb = RGBLED(red=led_pins[0], green=led_pins[1], blue=led_pins[2], active_high=True)

        self.btn_start.when_pressed = self.start_recording
        self.btn_stop.when_pressed = self.stop_recording

        self.monitor_thread = threading.Thread(target=self._status_monitor, daemon=True)
        self.monitor_thread.start()

    def start_recording(self):
        started = False
        for v in self.videos.values():
            if not v.recording:
                v.start()
                started = True

        if not self.audio.recording:
            self.audio.start()
            started = True

        if started:
            self._log("▶️ Старт з GPIO")

    def stop_recording(self):
        stopped = False
        for v in self.videos.values():
            if v.recording:
                v.stop()
                stopped = True

        if self.audio.recording:
            self.audio.stop()
            stopped = True

        if stopped:
            self._log("⏹️ Стоп з GPIO")
            # моргнути зеленим
            self.rgb.color = (0, 1, 0)
            time.sleep(1)
            self.rgb.color = (0, 0, 1)

    def _status_monitor(self):
        while True:
            recording = any(v.recording for v in self.videos.values()) or self.audio.recording
            if recording:
                self.rgb.color = (1, 0, 0)  # 🔴 Червоний
            else:
                self.rgb.color = (0, 0, 1)  # 🔵 Синій
            time.sleep(0.5)

    def _log(self, message):
        if self.gui:
            self.gui.update_status_label(message)
        print(message)

    def stop(self):
        self.rgb.off()
