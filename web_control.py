from flask import Flask, render_template, redirect, jsonify
import os, signal, subprocess, time

app = Flask(__name__)

proc1 = proc2 = None
recording = False
paused = False

@app.route('/')
def index():
    return render_template('index.html', recording=recording, paused=paused)

@app.route('/start')
def start():
    global recording, proc1, proc2, paused
    if recording:
        return redirect('/')

    date = time.strftime("%Y-%m-%d_%H-%M-%S")
    folder = f"/home/wytcorp/Projects/video_recorder/records/recording_{date}"
    os.makedirs(folder, exist_ok=True)

    cmd_cam1 = [
        "ffmpeg", "-f", "v4l2", "-input_format", "mjpeg", "-framerate", "30",
        "-video_size", "1920x1080", "-i", "/dev/video0",
        "-c:v", "copy", f"{folder}/cam1_{date}.mkv"
    ]

    cmd_cam2 = [
        "ffmpeg", "-f", "v4l2", "-input_format", "mjpeg", "-framerate", "30",
        "-video_size", "1920x1080", "-i", "/dev/video2",
        "-c:v", "copy", f"{folder}/cam2_{date}.mkv"
    ]

    proc1 = subprocess.Popen(cmd_cam1)
    proc2 = subprocess.Popen(cmd_cam2)

    recording = True
    paused = False

    return redirect('/')

@app.route('/pause')
def pause_recording():
    global paused
    if recording and not paused:
        proc1.send_signal(signal.SIGSTOP)
        proc2.send_signal(signal.SIGSTOP)
        paused = True
    return redirect('/')

@app.route('/resume')
def resume_recording():
    global paused
    if recording and paused:
        proc1.send_signal(signal.SIGCONT)
        proc2.send_signal(signal.SIGCONT)
        paused = False
    return redirect('/')

@app.route('/stop')
def stop():
    global recording, paused
    if recording:
        proc1.terminate()
        proc2.terminate()
        recording = False
        paused = False
    return redirect('/')

@app.route('/status')
def status():
    return jsonify({'recording': recording, 'paused': paused})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False)