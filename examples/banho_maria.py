from machine import Pin, Signal

from time import sleep

from board_manager import D2, D6
from sensor_manager import Sensor_DS18B20

print("Setting up Relay")

relay1_pin = Pin(D6, Pin.OUT)
relay1 = Signal(relay1_pin, invert=True)
relay1.off()

print("Setting up Temperature sensor")
sensor = Sensor_DS18B20(D2)

DELAY = 2

LIMITE_HIGH = 90
LIMITE_LOW = 85
LIMITE_HEAT = 0.01 * DELAY

sensor.read()

temps = [sensor.values[0], sensor.values[0]]
temps_index = 0
status, status_last = 0, 1

print(f"Temp; Status; Gradiente; Heat_Limit")
while True:
  sensor.read()
  if sensor.values:
      temps[temps_index] = sensor.values[0]
      gradient = (temps[1] - temps[0] ) / DELAY 
      if temps[1] > LIMITE_HIGH:
          status = 0
      elif temps[1] < LIMITE_LOW:
          if gradient < LIMITE_HEAT:
              status = 1
          else:
              status = 0
              
  if status != status_last:
      relay1.value(status)
      
  print(f"Temp: {temps[0]}; {status}; {round(gradient, 2)}; {LIMITE_HEAT}")
  sleep(DELAY)
  status_last = status
  temps_index = (temps_index + 1 ) % 2
