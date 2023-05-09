from time import sleep
from machine import Pin
from neopixel import NeoPixel

from board_manager import D2
np_size = 7
np = NeoPixel(Pin(D2), np_size)

vermelho = (255, 0, 0)
azul = (0, 0, 255)
roxo = (153, 51, 153)
preto = (0,0,0)

while True:
    for i in range(1, np_size):
        if i % 4 == 0:
            np[0] = azul
        else:
            np[0] = preto
            
        np[i] = azul
        np.write()
        sleep(0.1)
        #np[i] = preto
        #np.write()


