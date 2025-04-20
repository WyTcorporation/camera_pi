arecord -l
Приклад виводу:
card 1: USB [USB Audio], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0

Перевір, що звук точно є:
arecord -f cd -D hw:1,0 test.wav
aplay test.wav


arecord -l
**** List of CAPTURE Hardware Devices ****
card 0: WEBCAM [GENERAL WEBCAM], device 0: USB Audio [USB Audio]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
Тоді твій hw буде: hw:0,0

🔧 Перевір підтримувані формати:
arecord -D hw:0,0 --dump-hw-params

arecord -D hw:0,0 --dump-hw-params
Warning: Some sources (like microphones) may produce inaudible results
         with 8-bit sampling. Use '-f' argument to increase resolution
         e.g. '-f S16_LE'.
Recording WAVE 'stdin' : Unsigned 8 bit, Rate 8000 Hz, Mono
HW Params of device "hw:0,0":
--------------------
ACCESS:  MMAP_INTERLEAVED RW_INTERLEAVED
FORMAT:  S16_LE
SUBFORMAT:  STD
SAMPLE_BITS: 16
FRAME_BITS: 16
CHANNELS: 1
RATE: 16000
PERIOD_TIME: [2000 1000000]
PERIOD_SIZE: [32 16000]
PERIOD_BYTES: [64 32000]
PERIODS: [2 1000]
BUFFER_TIME: [4000 2000000]
BUFFER_SIZE: [64 32000]
BUFFER_BYTES: [128 64000]
TICK_TIME: ALL
--------------------
arecord: set_params:1352: Sample format non available
Available formats:
- S16_LE

🔁 Запиши тест вручну з правильними параметрами:

arecord -f cd -c1 -r 44100 -D hw:0,0 test.wav

-c1 = 1 канал
-r 44100 = 44100 Гц
-f cd = S16_LE, 44100Hz, стерео → але ми зменшуємо до -c1

