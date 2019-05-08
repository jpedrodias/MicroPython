# filename: main_oled.py
import os, gc, micropython, machine, time, json
from board_manager import D1, D2, D7

GATE_PIN = micropython.const(D7) # D7
GATE_MODE = micropython.const(0) # 0 for always on | 1 for always off
DEBUG = micropython.const(1) # Change from 1 debug mode to 0 production mode
DEBUG_TIME = micropython.const(10) # Run in debug mode for this amount of seconds
DELAY_TIME = micropython.const(1)  # Delay between loops

print('PhotoGate in MicroPython')

# ssd1306 version
import ssd1306
i2c = machine.I2C(scl=machine.Pin(D1), sda=machine.Pin(D2))
oled = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3c)

from sensor_manager import PhotoGate
g1 = PhotoGate(GATE_PIN, mode=GATE_MODE) # mode = 1 | 0

oled.fill(0)
oled.rect(0,0,128,40,1)
oled.text('PhotoGate', 28, 8)
oled.text('in MicroPython', 10, 24)
oled.text('in milli seconds', 00, 56)
oled.show()

def update_oled(data):
  oled.scroll(0, -8)
  oled.fill_rect(0, 56, 128, 64, 0)
  oled.text('{:10.3f}'.format(data), 0, 56)
  oled.show()

gc.collect()
while True:
  g1.read()

  if g1.event_change_to(1):
    g1.start_time()
  if g1.event_change_to(0):
    g1.stop_time()
    print(g1.millis)
    update_oled(g1.millis)
  g1.store()
  if DEBUG:
    time.sleep_us(DEBUG_TIME)
  else:
    time.sleep_us(DELAY_TIME)
#End while loops 
