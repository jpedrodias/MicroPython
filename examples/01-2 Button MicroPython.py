from machine import Pin
from time import sleep
 
D4 = 2 # to connect to the button
D3 = 0 # to connect to the button
D2 = 4 # to connect to the green led
D1 = 5 # to connect to the red led

# OutPut
green = Pin( D2, Pin.OUT ) 
red = Pin( D1, Pin.OUT )

# Input
btn1 = Pin(D3, Pin.IN)

last_value = 1
while True:
  value = btn1.value()
  if value != last_value:
    green.value( value )
    red.value( not value )
  last_value = value
  sleep(0.5)
