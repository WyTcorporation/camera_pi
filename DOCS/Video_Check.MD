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