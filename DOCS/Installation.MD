Інструкція: Запис відео з двох USB-камер на Raspberry Pi 5
📌 Завдання:

Raspberry Pi 5 з двома USB 3.0 камерами

Одночасний запис відео у високій якості

Фізичні кнопки старт, стоп, пауза, індикатор

Запис на зовнішній диск (SSD/USB-накопичувач)

📌 Підготовка обладнання та софту (етап 1)
🛒 Перелік обладнання:
Raspberry Pi 5 (8GB RAM рекомендовано)

MicroSD карта (мінімум 32GB)

2 × USB 3.0 камери (наприклад, Aoni або ELP)

USB 3.0 SSD або флешка (мінімум 128GB)

Адаптер живлення (5V / 5A USB-C)

Ethernet кабель / Wi-Fi

3 кнопки, 1 світлодіод, резистор 220Ω, макетка (для GPIO)

📥 1. Встановлення Raspberry Pi OS (64-bit)
Завантаж офіційний образ Raspberry Pi OS Lite (64-bit)

Запиши образ на карту через:

Windows: Raspberry Pi Imager

Linux: dd або Balena Etcher

⚠️ Важливо:
Під час запису, активуй SSH, налаштуй Wi-Fi через Raspberry Pi Imager (Advanced Options).

📌 2. Перший запуск та налаштування
Встав SD-карту у Raspberry Pi.

Підключи Ethernet або увімкни Wi-Fi.

Підключись до Pi через SSH:

```
    ssh pi@<IP-адреса>
    # пароль: raspberry
```

Оновлення ОС:
```
    sudo apt update && sudo apt upgrade -y
    sudo reboot
```

3. Підготовка USB-камер
Підключи дві USB-камери до USB 3.0 портів Pi.

Перевір, що камери бачить система:

```ls /dev/video*```

Повинні з’явитись:

```
/dev/video0
/dev/video1
```

🛠️ Встанови інструменти для роботи з камерами:

```sudo apt install v4l-utils ffmpeg -y```

📹 Перевір кожну камеру окремо:

```v4l2-ctl --list-devices```

Отримуєш список пристроїв та назв.

📸 Перевір відеопотік (опціонально):

```
ffplay /dev/video0
ffplay /dev/video1
```

4. Підготовка USB-накопичувача (SSD/USB-флешка)
Підключи SSD/флешку до USB.

Перевір наявність пристрою:

```sudo lsblk```

Приклад:

sda
 └─sda1

Форматуємо та монтуємо накопичувач:
(💡 Припустимо, що це /dev/sda1)

Якщо потрібен формат (FAT32 для сумісності з Windows, ext4 для Linux):

```
    sudo mkfs.ext4 /dev/sda1
    # або для FAT32:
    sudo mkfs.vfat /dev/sda1
```


Створюємо точку монтування:

```
    sudo mkdir -p /mnt/usb
    sudo mount /dev/sda1 /mnt/usb
```

Автоматичне монтування:

```sudo nano /etc/fstab```

Додай рядок (приклад для ext4):

```/dev/sda1 /mnt/usb ext4 defaults,nofail 0 0```

Для FAT32:

```/dev/sda1 /mnt/usb vfat defaults,nofail 0 0```

Перевір:

```sudo reboot```

Після перезавантаження перевір:

```df -h```

Побачиш /mnt/usb.

desktop
chmod +x ~/Projects/video_recorder/start.sh
Скопіювати файл .desktop у папку:
```~/.local/share/applications/video_recorder.desktop```
Оновити меню
```update-desktop-database ~/.local/share/applications/```


