
# 📦 Raspberry Pi DualCam Recorder — Повний DIY-комплекс

Цей проект створює автономну систему відеозапису на базі Raspberry Pi 5 з двома камерами USB, звуком, графічним інтерфейсом (PyQt6), вебінтерфейсом (FastAPI), та апаратним керуванням (GPIO).

---

## 📋 Основні можливості:

- 🎥 Запис відео з двох камер одночасно
- 🎙️ Запис звуку з USB-мікрофону
- 🖥️ PyQt6 інтерфейс з превʼю
- 🌐 Вебінтерфейс керування (FastAPI + HTML/JS)
- 🔘 Кнопки GPIO: Старт / Стоп
- 🔴 RGB-LED індикатор: статус запису
- 🔐 Повністю офлайн, без хмар
- 📁 Структуроване збереження записів

---

## ⚙️ Встановлення

1. **Підготуй Raspberry Pi:**
   - ОС: Raspberry Pi OS 64-bit
   - Python ≥ 3.11
   - Установи базові пакети:
     ```bash
     sudo apt update && sudo apt install python3-pyqt6 python3-opencv python3-gpiozero python3-fastapi python3-pip -y
     ```

2. **Запуск графічного інтерфейсу:**
   - Створи ярлик `video_recorder.desktop` у `~/.local/share/applications`
   - Вказівка:
     ```bash
     Exec=python3 /home/pi/Projects/video_recorder/main.py
     ```

3. **Автозапуск вебінтерфейсу:**
   - Додається автоматично в бекграунді через FastAPI (`uvicorn`)
   - За замовчуванням доступно: http://<IP>:8080/

---

## 🧩 Структура проекту

```
video_recorder/
├── core/
│   ├── recorder.py
│   ├── audio.py
│   ├── webserver.py
│   ├── gpio.py
├── gui/
│   └── main_window.py
├── static/
│   ├── css/
│   └── js/
├── templates/
│   └── index.html
├── main.py
├── start.sh
└── README.md
```

---

## 🚦 GPIO:

- Кнопка Старт: `GPIO 17`
- Кнопка Стоп: `GPIO 22`
- RGB-LED:
  - R: `GPIO 5`
  - G: `GPIO 6`
  - B: `GPIO 13`

---

## 🗂️ Записи:

Зберігаються в:
```
~/Projects/video_recorder/records/recording_YYYY-MM-DD_HH-MM-SS/
```

---

## 🤝 Автор проєкту:

DIY-мастер Владислав 
