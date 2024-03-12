from neopixel import NeoPixel
from machine import Pin
from time import sleep
from board_manager import D2

class Color:
    # RGB - Red, Green, Blue
    X= 50 # 0 - 255 # brightness
    R = (X, 0, 0)
    G = (0, X, 0)
    B = (0, 0, X)
    BK = (0,0,0)

num_pixeis = 1
neo = NeoPixel(Pin(D2), num_pixeis)
neo.fill(Color.BK)
neo.write()

PAUSE = 1 # CHANGE THIS VALUE
DURATION = 10 # seconds
colors = [Color.R, Color.G, Color.B]
#colors = [Color.R, Color.G]
#colors = [Color.G, Color.B]
#colors = [Color.R, Color.B]

ncolors = len(colors)

for i in range(int(DURATION / PAUSE)):
  neo.fill(colors[i % ncolors])
  neo.write()
  sleep(PAUSE)

neo.fill(Color.BK)
neo.write()
