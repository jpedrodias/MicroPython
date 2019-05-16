# filename: main_photogate.py
import os, gc, micropython, machine, time
from board_manager import D7

GATE_PIN = D7
GATE_MODE = micropython.const(0) # 0 for always on | 1 for always off
DEBUG = micropython.const(1) # Change from 1 debug mode to 0 production mode
DEBUG_TIME = micropython.const(10) # Run in debug mode for this amount of seconds
DELAY_TIME = micropython.const(1)  # Delay between loops

print('PhotoGate in MicroPython')

from sensor_manager import PhotoGate
gate1 = PhotoGate(GATE_PIN, mode=GATE_MODE) # mode = 1 | 0

gc.collect()
while True:
  gate1.read()
  if gate1.event_change_to(1):
    gate1.start_time()
  if gate1.event_change_to(0):
    gate1.stop_time()
    print(gate1.millis)
  gate1.store()
  if DEBUG:
    time.sleep_us(DEBUG_TIME)
  else:
    time.sleep_us(DELAY_TIME)
#End while loop
