# filename: main_ds18b20_oled.py
import os, gc, micropython, machine, time, json
from board_manager import D1 as SCL, D2 as SDA, D7

DEBUG = micropython.const(1) # Change from 1 debug mode to 0 production mode
DEBUG_TIME = micropython.const(10) # Run in debug mode for this amount of seconds
DELAY_TIME = micropython.const(10)  # Delay between loops

print('DS18B20 in MicroPython')

# ssd1306 version
import ssd1306
i2c = machine.I2C(scl=machine.Pin(SCL), sda=machine.Pin(SDA))
oled = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3c)

from sensor_manager import Sensor_DS18B20
sensor = Sensor_DS18B20(D7)

oled.fill(0)
oled.rect(0,0,128,40,1)
oled.text('PhotoGate', 28, 8)
oled.text('in MicroPython', 10, 24)
oled.text('in milli seconds', 00, 56)
oled.show()

def update_oled(data):
  oled.scroll(0, -8)
  oled.fill_rect(0, 56, 128, 64, 0)
  oled.text('{}'.format(data), 0, 56)
  oled.show()

gc.collect()
while True:
  sensor.read()
  
  msg = ''
  for key, value in sensor.values_dict.items():
    msg += '{}: {}'.format(key, value)
  print(msg)
  update_oled(msg)
  
  if DEBUG:
    time.sleep(DEBUG_TIME)
  else:
    time.sleep(DELAY_TIME)
#End while loops 
