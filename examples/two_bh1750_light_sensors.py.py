from machine import Pin, I2C
from time import sleep

from board_manager import D1, D2 # D1, ... , D8
from sensor_manager import Sensor_BH1750FVI
from ssd1306 import SSD1306_I2C

# Inter-Integrated Circuit (I2C) Protocol
i2c = I2C(scl=Pin(D1), sda=Pin(D2)) # i2c.scan()

# Light Sensor bh1750 - i2c address 0x23 (35) and 0x5c (92)
sensor1 = Sensor_BH1750FVI(i2c, address=0x23)
sensor2 = Sensor_BH1750FVI(i2c, address=0x5c)

# OLED Display 0.96' - size 168x64
oled = SSD1306_I2C(128, 64, i2c, 0x3c) # 60


def oled_print_center(msg, line, shift=0):
    pos = (128-shift-len(msg)*8)//2
    oled.text(msg, pos, line)
    
def oled_print(value1=65535, value2=65535):
    oled.fill(0)
    oled.rect(0,0,128,64,1)
    oled.rect(0,0,128,20,1)
    oled.text('Light Sensor', 16, 8)
    oled_print_center(f'{value1} lux', 28)
    oled_print_center(f'{value2} lux', 46)
    oled.show()

while True:
    value1 = sensor1.read()
    value2 = sensor2.read()
    
    oled_print(value1, value2)
    sleep(1)
