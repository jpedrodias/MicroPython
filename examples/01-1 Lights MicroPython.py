from machine import Pin
from time import sleep

D4 = 2 
D3 = 0 # to connect to the green led
D2 = 4 # to connect to the yellow led
D1 = 5 # to connect to the red led

green = Pin( D3, Pin.OUT )
yellow = Pin( D2, Pin.OUT )
red = Pin( D1, Pin.OUT )

loops = 3
while loops > 0:
  green.on()
  sleep( 1 )
  green.off()
  yellow.on()
  sleep( 1 )
  yellow.off()
  red.on()
  sleep( 1 )
  red.off()
  loops = loops - 1 # comment this line to run forever

