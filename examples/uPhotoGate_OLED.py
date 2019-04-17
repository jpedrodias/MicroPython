# WEMOS D1 Mini Board GPIO Map: D8 pull_down, D4 pull_down
# D0=16, D1=5, D2=4, D3=0, D4=2, D5=14, D6=12, D7=13, D8=15
import os, gc, micropython, machine, time, json

GATE_PIN = micropython.const(13) # D7
GATE_MODE = micropython.const(0) # 0 for always on | 1 for always off
DEBUG = micropython.const(1) # Change from 1 debug mode to 0 production mode
DEBUG_TIME = micropython.const(10) # Run in debug mode for this amount of seconds
DELAY_TIME = micropython.const(1)  # Delay between loops


print('PhotoGate in MicroPython - v0.1')


# ssd1306 version
import ssd1306
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3c)

from sensor_manager import PhotoGate
g1 = PhotoGate(GATE_PIN, mode=GATE_MODE) # mode = 1 | 0
BSIZE = micropython.const(8)
data = list(0.0 for i in range(BSIZE))
CURLINED = {True: 'ms>', False: '   '}
CURLINE = 0
  
oled.fill(0)
oled.text('PhotoGate', 24, 8)
oled.text('in MicroPython', 10, 24)
oled.text('in milli seconds', 00, 56)
oled.show()

def update_oled():
  oled.fill(0)
  for i in range(BSIZE):
    cl = CURLINED[i == 7] # 
    vi = (i + BSIZE + CURLINE + 1) % BSIZE # Virtual Index
    oled.text('{} {:.3f}'.format(cl, data[vi]), 0, i * 8)
  oled.show()
  
while True:
  g1.read()
  if g1.event_change_to(1):
    g1.start_time()
  if g1.event_change_to(0):
    g1.stop_time()
    data[CURLINE] = g1.show_ms()
    print(g1.show_ms(),'ms')
    update_oled()
    CURLINE = ( CURLINE + 1 ) % BSIZE
  g1.store()
  time.sleep_us(DELAY_TIME)
#End while loops
  
#if __name__ == '__main__':
#  main_oled()
