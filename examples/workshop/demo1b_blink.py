# filename: demo1b_blink.py
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
