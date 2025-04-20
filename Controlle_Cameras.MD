Підключення фізичних кнопок та світлодіода для керування
📌 Що буде зроблено:
Кнопка Старт: початок запису

Кнопка Пауза: призупинення запису

Кнопка Стоп: завершення запису

LED-індикатор запису

⚙️ 1. Підготовка компонентів:
📋 Список компонентів:
3 × тактові кнопки (будь-які, наприклад, 6х6мм)

1 × світлодіод (червоний або зелений)

1 × резистор (220Ω для світлодіода)

Проводи (Dupont, макетка)

⚡ 2. Схема підключення GPIO:
Використовуємо фізичні піни GPIO на Raspberry Pi 5.

Компонент	GPIO BCM номер	Фізичний пін
Старт	GPIO17	11
Пауза	GPIO22	15
Стоп	GPIO27	13
Світлодіод	GPIO23	16
Земля (GND)	-	6,9,14,20,25

🎯 Фізичне підключення:

Pi GPIO17 (пін 11) → Кнопка Старт → GND
Pi GPIO22 (пін 15) → Кнопка Пауза → GND
Pi GPIO27 (пін 13) → Кнопка Стоп → GND
Pi GPIO23 (пін 16) → Резистор 220Ω → (+) світлодіод (-) → GND

Важливо:

Використовуємо внутрішні підтягуючі резистори GPIO.
Кнопки підключаються до GPIO і GND без додаткових резисторів.

🛠️ 3. Перевірка підключення (необов'язково, але рекомендую):
Перевір, що все працює:

```

    sudo apt install python3-gpiozero
    python3 
```

Тест 

```
    from gpiozero import Button, LED
    from signal import pause
    
    btn_start = Button(17)
    btn_pause = Button(22)
    btn_stop = Button(27)
    led = LED(23)
    
    btn_start.when_pressed = lambda: print("Старт натиснуто!")
    btn_pause.when_pressed = lambda: print("Пауза натиснуто!")
    btn_stop.when_pressed = lambda: print("Стоп натиснуто!")
    
    led.on() # Світлодіод засвітиться
    pause()
```
Натискай кнопки і побачиш повідомлення.
LED має засвітитись.

📜 4. Основний Python-скрипт запису відео:
Створимо папку та скрипт:

```
    mkdir ~/video_recorder
    cd ~/video_recorder
    nano recorder.py
```

🖥️ Код основного скрипту (recorder.py):

```
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
        folder = f"/mnt/usb/recording_{date}"
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

```

Запуск для тесту:
```
    python3 recorder.py
```

🚀 5. Автозапуск скрипту при старті ОС (опціонально)

```sudo nano /etc/rc.local```

Додай перед рядком exit 0:

```python3 /home/pi/video_recorder/recorder.py &```

🎬 Перевірка роботи:
Натискай кнопки Старт, Пауза, Стоп.

Відео повинні зберігатись у папку /mnt/usb.
