from gpiozero import Button, LED
import threading
import time

class GPIOController:
    def __init__(self, video_recorder, audio_recorder, button_pin=17, led_pin=27):
        self.video = video_recorder
        self.audio = audio_recorder
        self.button = Button(button_pin, pull_up=True, bounce_time=0.1)
        self.led = LED(led_pin)

        self.button.when_pressed = self.toggle_recording

    def toggle_recording(self):
        if not self.video.recording:
            self.video.start()
            self.audio.start()
            self.led.on()
        else:
            self.video.stop()
            self.audio.stop()
            self.led.off()

    def stop(self):
        self.led.off()
