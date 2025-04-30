📋 План:
1. ⚙️ Підготувати NAS:
Встановити FreeNAS / TrueNAS або OpenMediaVault.

Налаштувати спільну папку (SMB share) для запису відео.

Встановити правильні права доступу.

2. 📡 Налаштувати Raspberry Pi:
Встановити клієнт cifs-utils.

Автоматично монтувати папку при запуску.

Змінити save_dir у Python-проєкті.

3. 📦 Забезпечити стабільну синхронізацію і безпечне збереження.
🛠️ Детальна інструкція
1. Налаштування NAS:
🔵 Встановлення FreeNAS/TrueNAS/OpenMediaVault:
Вибери систему. Я рекомендую TrueNAS SCALE — бо:

Легка.

Підтримує ZFS.

Має Web-інтерфейс.

Підтримує SMB для Raspberry Pi.

🔹 Якщо хочеш — допоможу і з установкою.

🔵 Створення SMB спільної папки:
Створити користувача piuser, пароль pipass (або свої).

Створити папку для записів:

Назва: recordings

Шлях: /mnt/data/recordings

Налаштувати розшарювання:

Відкрити доступ через SMB (Windows share).

Дати права на читання/запис користувачу piuser.

Адреса папки:
//NAS_IP/recordings
2. Налаштування Raspberry Pi:
🔵 Встановити cifs-utils:

sudo apt update
sudo apt install cifs-utils -y

🔵 Створити папку для монтування:
sudo mkdir -p /mnt/nas

📋 Перевірка
З Raspberry Pi перевір:
smbclient -L //192.168.x.x -U piuser
Після чого можеш монтувати:
sudo mount -t cifs -o username=piuser,password=pass,vers=3.0 //192.168.1.111/recordings /mnt/nas
Для автозавантаження після перезавантаження, додай у /etc/fstab на Pi:
# NAS recordings
//192.168.1.111/recordings  /mnt/nas  cifs  username=piuser,password=pass,vers=3.0,iocharset=utf8,uid=1000,gid=1000  0  0


🔵 Спробувати ручне монтування:
sudo mount -t cifs -o username=piuser,password=pass,vers=3.0 //192.168.1.111/recordings /mnt/nas
//192.168.1.111/recordings  /mnt/nas  cifs  credentials=/home/pi/.smbcredentials,vers=3.0,iocharset=utf8,uid=1000,gid=1000,nofail,x-systemd.automount  0  0

mount | grep cifs
or 
lsblk -f
sudo umount /mnt/nas

sudo mount -t cifs -o username=piuser,password=pass,vers=3.0 //192.168.1.111/recordings /mnt/nas

//192.168.1.111/recordings /mnt/nas cifs username=piuser,password=pass,vers=3.0,iocharset=utf8,nofail 0 0

smbclient //192.168.1.111/recordings -U piuser
sudo nano /etc/fstab

sudo nano /etc/samba/credentials
username=piuser
password=pass

sudo chmod 600 /etc/samba/credentials
sudo chown -R piuser:piuser /mnt/nas

sudo nano /etc/fstab
# NAS mount
//192.168.1.111/recordings /mnt/nas cifs credentials=/etc/samba/credentials,uid=1000,gid=1000,vers=3.0,iocharset=utf8,nofail 0 0

sudo chown -R piuser:piuser /mnt/nas
