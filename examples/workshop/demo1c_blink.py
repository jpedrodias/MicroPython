# filename: demo1c_blink.py
from machine import Pin
from time import sleep
 
PINS = [10, 11, 12]
pause = 1

LEDS = [Pin(pin, Pin.OUT) for pin in PINS]
 
loops = 3
while loops > 0:
    for led in LEDS:
        for status in [1, 0]:
            led.value(status)
            sleep(pause * status)

    loops = loops - 1 # comment this line to run forever
