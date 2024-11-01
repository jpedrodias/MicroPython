# filename: demo3a_ultrasonic.py
from machine import Pin
from time import sleep_ms
from sensor_manager import Sensor_HCSR04

LED_PINS = [10, 11, 12]
PIN_TRIGGER, PIN_ECHO = 16, 17

LEDS = [Pin(pin, Pin.OUT) for pin in LED_PINS]

sensor = Sensor_HCSR04(trigger=PIN_TRIGGER, echo=PIN_ECHO)

while True:
    sensor.read()
    d = sensor.distance_mm
    if d > 100:
        nleds = 0
    elif d > 50:
        nleds = 1
    else:
        nleds = 2
    
    for index, led in enumerate(LEDS):
        value = 1 if index == nleds else 0
        LEDS[index].value(value)
    sleep_ms(50)
