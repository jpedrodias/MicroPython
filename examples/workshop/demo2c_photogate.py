# filename: demo2c_photogate.py
from machine import Pin
from time import sleep_ms
from sensor_manager import PhotoGate

PIN_G = 10 # to connect to the green led
PIN_R = 11 # to connect to the red led
PIN_GATE = 14 # to connect to the obstacle sensor
PIN_GATE_MODE = 1 # 0 for always on | 1 for always off

led_g = Pin( PIN_G, Pin.OUT )
led_r = Pin( PIN_R, Pin.OUT )
gate1 = PhotoGate( PIN_GATE, mode=PIN_GATE_MODE )

while True:
    gate1.read()
    if gate1.event_change_to(1):
        gate1.start_time()
        led_g.value(0)
        led_r.value(1)
    if gate1.event_change_to(0):
        gate1.stop_time()
        led_g.value(1)
        led_r.value(0)
        print(gate1.millis)
    gate1.store()

