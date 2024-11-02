# MicroPython Workshop - 2024-11-06 @ ISP


## Demo 1a - Digital output - Blink
![Demo 1a](https://github.com/user-attachments/assets/af4d2c6e-24a3-4919-a20c-a1978e68c92e=){: style="height:83px"}
```Python
# filename: demo1a_blink.py
from machine import Pin
from time import sleep
 
PIN_G = 10 # Green pin

pause = 1

led_g = Pin( PIN_G, Pin.OUT ) 

loops = 3
while loops > 0:
    led_g.on()
    sleep(pause)
    led_g.off()
    sleep(pause)
    loops = loops - 1 # comment this line to run forever
```
