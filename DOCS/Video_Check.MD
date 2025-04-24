sudo apt install v4l-utils
v4l2-ctl --list-devices
v4l2-ctl --device=/dev/video0 --list-formats-ext
Це видасть приблизно таке:
[0]: 'MJPG' (Motion-JPEG)
    Size: Discrete 1920x1080
        Interval: Discrete 0.033s (30.000 fps)
    Size: Discrete 1280x720
        Interval: Discrete 0.033s (30.000 fps)

Як оцінити мегапікселі:
1920 × 1080 = 2 073 600 → 2 Мп
1280 × 720 = 921 600 → ~0.9 Мп

Фіксація експозиції та балансу білого: Встановіть ці параметри вручну, щоб уникнути коливань яскравості та кольору:​
v4l2-ctl -d /dev/video2 --set-ctrl=exposure_auto=1
v4l2-ctl -d /dev/video2 --set-ctrl=exposure_absolute=200
v4l2-ctl -d /dev/video2 --set-ctrl=white_balance_temperature_auto=0
v4l2-ctl -d /dev/video2 --set-ctrl=white_balance_temperature=4500


Пробовал 

Додай перед self.writer.write(frame):
frame = cv2.rotate(frame, cv2.ROTATE_180)
та
frame = cv2.flip(frame, 1)  # 0 = вертикально, 1 = горизонтально, -1 = і те, і те

🔄 Повернути на 180°	cv2.rotate(frame, cv2.ROTATE_180)
↕️ Перевернути по Y	cv2.flip(frame, 0)
↔️ Віддзеркалити по X	cv2.flip(frame, 1)
🔃 Обидва напрямки	cv2.flip(frame, -1)

Вирішив поки не гратися