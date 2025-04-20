import RPi.GPIO as GPIO
import threading
import time

class GPIOController:
    def __init__(self, video_recorder, audio_recorder, button_pin=17, led_pin=27):
        self.video = video_recorder
        self.audio = audio_recorder
        self.button_pin = button_pin
        self.led_pin = led_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.led_pin, GPIO.OUT)

        self._running = True
        self._thread = threading.Thread(target=self._watch_button, daemon=True)
        self._thread.start()

    def _watch_button(self):
        last_state = GPIO.input(self.button_pin)
        while self._running:
            current_state = GPIO.input(self.button_pin)
            if last_state == GPIO.HIGH and current_state == GPIO.LOW:
                self.toggle_recording()
            last_state = current_state
            time.sleep(0.1)

    def toggle_recording(self):
        if not self.video.recording:
            self.video.start()
            self.audio.start()
            GPIO.output(self.led_pin, GPIO.HIGH)
        else:
            self.video.stop()
            self.audio.stop()
            GPIO.output(self.led_pin, GPIO.LOW)

    def stop(self):
        self._running = False
        GPIO.cleanup([self.button_pin, self.led_pin])
