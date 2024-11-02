# MicroPython Workshop - 2024-11-06 @ ISP


## Demo 1a - Digital output - Blink

![image](./img/Semaforo%20-%20Pi%20Pico_bb.png)

<img src="./img/Semaforo%20-%20Pi%20Pico_bb.png" alt="demo1a" width="250"/>

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
