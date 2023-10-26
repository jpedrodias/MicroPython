from neopixel import NeoPixel
from machine import Pin
from time import sleep
from board_manager import D7

class Color:
    # RGB - Red, Green, Blue
    brightness = 50 # 0 - 255
    R = (brightness, 0, 0)
    G = (0, brightness, 0)
    B = (0, 0, brightness)
    BK = (0,0,0)
    
neo = NeoPixel(Pin(D7), 1)
neo.fill(Color.BK)
neo.write()

PAUSE = 0.5 # CHANGE THIS VALUE
DURATION = 10 # seconds
colors = [Color.R, Color.G, Color.B]
#colors = [Color.R, Color.G]
#colors = [Color.G, Color.B]
#colors = [Color.R, Color.G]
ncolors = len(colors)

for i in range(int(DURATION / PAUSE)):
  neo.fill(colors[i%ncolors])
  neo.write()
  sleep(PAUSE)

neo.fill(Color.BK)
neo.write()
