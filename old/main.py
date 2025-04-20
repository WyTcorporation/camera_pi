import subprocess, os, signal, time
from gpiozero import Button, LED
from signal import pause

# GPIO-кнопки та LED
btn_start = Button(17, bounce_time=0.2)
btn_pause = Button(22, bounce_time=0.2)
btn_stop = Button(27, bounce_time=0.2)
led = LED(23)

recording = False
paused = False
proc1 = proc2 = None

def start_recording():
    global recording, proc1, proc2
    if recording:
        print("Запис вже триває.")
        return

    date = time.strftime("%Y-%m-%d_%H-%M-%S")
    folder = f"/home/wytcorp/Projects/video_recorder/records/recording_{date}"
    os.makedirs(folder, exist_ok=True)

    cmd_cam1 = [
        "ffmpeg",
        "-f", "v4l2", "-input_format", "mjpeg", "-framerate", "30",
        "-video_size", "1920x1080", "-i", "/dev/video0",

        "-f", "alsa", "-ac", "2", "-i", "hw:1,0",

        "-c:v", "libx264", "-preset", "ultrafast",
        "-c:a", "aac", "-b:a", "128k",
        f"{folder}/cam1_{date}.mp4"
    ]

    cmd_cam2 = [
        "ffmpeg", "-f", "v4l2", "-input_format", "mjpeg", "-framerate", "30",
        "-video_size", "1920x1080", "-i", "/dev/video2",
        "-c:v", "copy", f"{folder}/cam2_{date}.mkv"
    ]

    proc1 = subprocess.Popen(cmd_cam1)
    proc2 = subprocess.Popen(cmd_cam2)

    recording = True
    led.on()
    print("Запис розпочато.")

def pause_recording():
    global paused
    if recording and not paused:
        proc1.send_signal(signal.SIGSTOP)
        proc2.send_signal(signal.SIGSTOP)
        paused = True
        led.blink()
        print("Запис на паузі.")

def resume_recording():
    global paused
    if recording and paused:
        proc1.send_signal(signal.SIGCONT)
        proc2.send_signal(signal.SIGCONT)
        paused = False
        led.on()
        print("Запис продовжено.")

def stop_recording():
    global recording, paused
    if recording:
        proc1.terminate()
        proc2.terminate()
        recording = False
        paused = False
        led.off()
        print("Запис зупинено.")

# Прив'язка кнопок
btn_start.when_pressed = start_recording
btn_pause.when_pressed = lambda: pause_recording() if not paused else resume_recording()
btn_stop.when_pressed = stop_recording

print("Система готова до роботи. Очікування натискання кнопок...")
pause()
