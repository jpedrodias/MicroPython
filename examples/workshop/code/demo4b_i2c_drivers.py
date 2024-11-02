# filename: demo4b_i2c_drivers.py
from machine import Pin, I2C
from time import sleep
import gc

# https://github.com/micropython/micropython-lib/blob/master/micropython/drivers/display/ssd1306/ssd1306.py
from ssd1306 import SSD1306_I2C

# https://github.com/kevbu/micropython-bme280/blob/master/bme280.py
from bme280 import BME280

gc.enable()

i2c_sda = 12
i2c_scl = 13

i2c = I2C(0,sda=i2c_sda,scl=i2c_scl)
oled = SSD1306_I2C(128, 64, i2c, addr=0x3C)
sensor = BME280(i2c=i2c, address=0x76)

while True:
    t = sensor.temperature()
    p = sensor.pressure()
    h = sensor.humidity()
    oled.fill(0)  # Clear the display
    oled.rect(0,0,128,64,1)
    oled.text("Temp: {}C".format(round(t, 1)), 0, 8)
    oled.text("Press: {}hPa".format(round(p, 1)), 0, 24)
    oled.text("Hum: {}%".format(round(h, 0)), 0, 38)
    oled.show()
    sleep(1)
