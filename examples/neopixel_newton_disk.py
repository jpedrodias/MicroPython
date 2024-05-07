from neopixel import NeoPixel
from machine import Pin
from time import sleep
from board_manager import D2

class Color:
  # RGB - Red, Green, Blue
  X = 50 # CHANGE THIS VALUE between 0 and 255 # brightness
  R = (X, 0, 0)  # RED
  G = (0, X, 0)  # GREEN
  B = (0, 0, X)  # BLUE
  BK = (0, 0, 0)  # BLACK

num_pixeis = 7
neo = NeoPixel(Pin(D2), num_pixeis)
neo.fill(Color.BK)
neo.write()

PAUSE = 1 # CHANGE THIS VALUE between 5 and 0.001 
DURATION = 10 # total time animation in seconds
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
