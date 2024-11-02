# MicroPython Workshop - 2024-11-06 @ ISP


## Demo 1a - Digital output - Blink
<img src="./img/demo1a_blink.png" alt="demo1a" width="250" align="left"/>

## filename: demo1a_blink.py
```Python:
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

---


## Demo 1b - Digital output - Blink
<img src="./img/demo1b_blink.png" alt="demo1a" width="250" align="left"/>

## filename: demo1b_blink.py
```Python:
from machine import Pin
from time import sleep
 
PIN_G = 10 # Green pin
PIN_Y = 11 # Yellow Pin
PIN_R = 12 # Red Pin
pause = 1
 
led_g = Pin( PIN_G, Pin.OUT )
led_y = Pin( PIN_Y, Pin.OUT )
led_r = Pin( PIN_R, Pin.OUT )
 
loops = 3
while loops > 0:
    led_g.on()
    sleep(pause)
    led_g.off()
    led_y.on()
    sleep(pause)
    led_y.off()
    led_r.on()
    sleep(pause)
    led_r.off()
    loops = loops - 1 # comment this line to run forever
```


---

