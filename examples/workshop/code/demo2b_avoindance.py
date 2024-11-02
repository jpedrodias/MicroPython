# filename: demo2b_avoindance.py
from machine import Pin
from time import sleep_ms

PIN_G = 10 # to connect to the green led
PIN_R = 11 # to connect to the red led
PIN_SENSOR = 14 # to connect to the obstacle sensor

led_g = Pin( PIN_G, Pin.OUT )
led_r = Pin( PIN_R, Pin.OUT )
sensor = Pin( PIN_SENSOR, Pin.IN )

last_value = 0
while True:
    value = sensor.value()
    if value != last_value:
        led_g.value( value )
        led_r.value( not value )
    last_value = value
    sleep_ms( 10 )
