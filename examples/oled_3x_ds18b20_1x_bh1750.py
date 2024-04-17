from machine import Pin, I2C
from time import sleep

from board_manager import D1, D2, D6, D3 # D1, ... , D8
from ssd1306 import SSD1306_I2C
from sensor_manager import Sensor_DS18B20
from sensor_manager import Sensor_BH1750FVI


btn = Pin(D6, Pin.IN)
# Inter-Integrated Circuit (I2C) Protocol
i2c = I2C(scl=Pin(D1), sda=Pin(D2)) # i2c.scan()

# OLED Display 0.96' - size 168x64
oled = SSD1306_I2C(128, 64, i2c, 0x3c) # 60

sensor_l = Sensor_BH1750FVI(i2c=i2c, address=0x23)
sensor_t = Sensor_DS18B20(D3)


def oled_print_center(msg, line, shift=0):
    pos = (128-shift-len(msg)*8)//2
    oled.text(msg, pos, line)
    #oled.show()
    
def oled_print(temps, lux):
    oled.fill(0)
    oled.rect(0,0,128,64,1)
    oled.rect(0,0,128,20,1)
    oled_print_center('C. ATLANTICO', 7)
    oled_print_temps(temps)
    lux = lux[0]
    oled_print_center(f'Light= {lux} lx', 52)
    oled.show()

def oled_print_temps(values):
    for i, value in enumerate(values):
        oled_print_center(f't{i+1}= {value} \'C', 24 + i*8)
    
while True:
    sensor_t.read()
    sensor_l.read()
    oled_print(sensor_t.values, sensor_l.values)
    sleep(1)
