Веб-інтерфейс керування записом
📌 Функціонал веб-інтерфейсу:
Старт / Пауза (перемикання)
Стоп
Статус запису (індикатор)

🛠️ 1. Встановлення Flask:

```
    sudo apt install python3-flask -y
```

📂 2. Структура проєкту:
Доповнимо існуючу папку:

```
    cd ~/video_recorder
    mkdir templates static
    nano web_control.py
```

🖥️ 3. Скрипт Flask веб-інтерфейсу (web_control.py):

```
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
    folder = f"~/Projects/video_recorder/records//recording_{date}"
    os.makedirs(folder, exist_ok=True)

    cmd_cam1 = ["ffmpeg", "-f", "v4l2", "-framerate", "30",
                "-video_size", "1920x1080", "-i", "/dev/video0",
                "-c:v", "libx264", "-preset", "veryfast",
                f"{folder}/cam1_{date}.mp4"]

    cmd_cam2 = ["ffmpeg", "-f", "v4l2", "-framerate", "30",
                "-video_size", "1920x1080", "-i", "/dev/video1",
                "-c:v", "libx264", "-preset", "veryfast",
                f"{folder}/cam2_{date}.mp4"]

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
```

🌐 4. HTML-інтерфейс (templates/index.html):

```
    nano templates/index.html
```

Додай код:

```
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <title>Raspberry Pi Video Control</title>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; padding: 50px; }
        button { padding: 15px 30px; margin: 10px; font-size: 20px; cursor: pointer; }
        .start { background: green; color: white; }
        .stop { background: red; color: white; }
        .pause { background: orange; color: black; }
    </style>
</head>
<body>
    <h1>Raspberry Pi Video Control</h1>

    {% if not recording %}
        <a href="/start"><button class="start">Старт</button></a>
    {% else %}
        {% if not paused %}
            <a href="/pause"><button class="pause">Пауза</button></a>
        {% else %}
            <a href="/resume"><button class="pause">Продовжити</button></a>
        {% endif %}
        <a href="/stop"><button class="stop">Стоп</button></a>
    {% endif %}

    <p>
        Статус запису: 
        {% if recording %}
            {% if paused %}
                <strong style="color:orange;">На паузі</strong>
            {% else %}
                <strong style="color:green;">Йде запис...</strong>
            {% endif %}
        {% else %}
            <strong style="color:red;">Запис зупинено</strong>
        {% endif %}
    </p>

    <script>
        setInterval(() => {
            fetch('/status').then(resp => resp.json()).then(data => {
                location.reload();
            });
        }, 5000);
    </script>
</body>
</html>

```

▶️ 5. Запуск веб-інтерфейсу:

```
    python3 web_control.py
```

🚀 6. Автозапуск веб-сервера при старті ОС:

```
    sudo nano /etc/rc.local
    
    #!/bin/sh -e
    cd /home/pi/video_recorder && python3 web_control.py &
    
    exit 0
```

```sudo chmod +x /etc/rc.local```

```ls -l /etc/rc.local```

Маєш побачити:
-rwxr-xr-x 1 root root ... /etc/rc.local
