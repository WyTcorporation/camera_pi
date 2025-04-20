arecord -l
Приклад виводу:
card 1: USB [USB Audio], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0

Перевір, що звук точно є:
arecord -f cd -D hw:1,0 test.wav
aplay test.wav

