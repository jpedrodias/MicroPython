# filename: demo2a_button.py
from machine import Pin
from time import sleep

PIN_G = 10 # Green pin
PIN_R = 11   # Red Pin
PIN_BTN = 14 

led_g = Pin( PIN_G, Pin.OUT )
led_r = Pin( PIN_R, Pin.OUT ) 
btn1 = Pin( PIN_BTN, Pin.IN )

led_g.on()
led_r.off()
last_value = 1
while True: 
    value = btn1.value()
    if value and value != last_value:
        led_g.value( not led_g.value() )
        led_r.value( not led_r.value() )
    last_value = value
    sleep( 0.1 )
