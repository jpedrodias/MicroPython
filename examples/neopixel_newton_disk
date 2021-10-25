from neopixel import NeoPixel
from machine import Pin
from time import sleep
from board_manager import D3

class Colors:
    # RGB - Red, Green, Blue
    brightness = 50
    RED = (255*brightness, 0, 0)
    GREEN = (0, 255*brightness, 0)
    BLUE = (0, 0, 255*brightness)
    BLACK = (0,0,0)
    
neo = NeoPixel(Pin(D3), 1)
neo.fill(Colors.BLACK)
neo.write()

PAUSE = 0.5 # CHANGE THIS VALUE
DURATION = 10 # seconds
colors = [Colors.RED, Colors.GREEN, Colors.BLUE]
ncolors = len(colors)

for i in range(int(DURATION / PAUSE)):
  neo.fill(colors[i%ncolors])
  neo.write()
  sleep(PAUSE)

neo.fill(Colors.BLACK)
neo.write()
