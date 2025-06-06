from neopixel import NeoPixel
from machine import Pin
from time import sleep
from board_manager import D2

class Color:
  # RGB - Red, Green, Blue
  X = 255
# CHANGE THIS VALUE between 0 and 255 # brightness
  R = (X, 0, 0)  # RED
  G = (0, X, 0)  # GREEN
  B = (0, 0, X)  # BLUE
  BK = (0, 0, 0)  # BLACK
  CY = (0, 247, 255)
  O = (255, 85, 0)
  Y = (255, 255, 0)

num_pixeis = 7
neo = NeoPixel(Pin(D2), num_pixeis)
neo.fill(Color.BK)
neo.write()

PAUSE = 0.001 # CHANGE THIS VALUE between 5 and 0.001 
DURATION = 6 # total time animation in seconds


colors1 = [Color.R, Color.G, Color.B]
colors2 = [Color.R, Color.G] # Amarelo
colors3 = [Color.G, Color.B] # Ciano
colors4 = [Color.R, Color.B] # Magenta

animations =  [
    {'pause': 1, 'colors': colors1, 'msg': 'R+G+B'},
    {'pause': 0.001, 'colors': colors1, 'msg': 'R+G+B'},

    {'pause': 1, 'colors': colors2, 'msg': 'R+G'},
    {'pause': 0.001, 'colors': colors2, 'msg': 'R+G'},

    {'pause': 1, 'colors': colors3, 'msg': 'G+B'},
    {'pause': 0.001, 'colors': colors3, 'msg': 'G+B'},

    {'pause': 1, 'colors': colors4, 'msg': 'R+B'},
    {'pause': 0.001, 'colors': colors4, 'msg': 'R+B'},
]

while True:
    for animation in animations:
        PAUSE = animation.get('pause')
        colors = animation.get('colors')
        msg = animation.get('msg', '')
        print(f'Disco de Newton - CORES: {msg} - PAUSA: {PAUSE}s')
        ncolors = len(colors)
        for i in range(int(DURATION / PAUSE)):
          color = colors[i % ncolors]
          neo.fill(color)
          neo.write()
          sleep(PAUSE)
        neo.fill(Color.BK)
        neo.write()
        sleep(1)

    neo.fill(Color.BK)
    neo.write()

