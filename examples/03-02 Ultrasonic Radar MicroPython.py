from machine import Pin
from time import sleep_ms
from board_manager import *
from sensor_manager import Sensor_HCSR04

green= Pin(D4, Pin.OUT)
red= Pin(D3, Pin.OUT)
sensor = Sensor_HCSR04(D1, D2)

LIMITE_DISTANCE = 10
while True:
  sensor.read()
  d = sensor.distance_cm
  if d > LIMITE_DISTANCE :
    green.on()
    red.off()
  else:
    green.off()
    red.on()
