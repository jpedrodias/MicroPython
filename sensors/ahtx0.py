# changed from https://github.com/vjsyong/AHT10/blob/master/aht10.py
# https://github.com/targetblank/micropython_ahtx0/blob/master/ahtx0.py

import time
from math import log

# AHT10 Library for MicroPython on ESP32
# Author: Sean Yong
# Date: 23rd December, 2019
# Version 1.0

class AHT10:
  AHT10_READ_DELAY_MS = 75 # Time it takes for AHT to collect data
  AHT_TEMPERATURE_CONST = 200
  AHT_TEMPERATURE_OFFSET = 50
  KILOBYTE_CONST = 1048576
  CMD_INITIALIZE = bytearray([0xE1, 0x08, 0x00])
  CMD_MEASURE = bytearray([0xAC, 0x33, 0x00])

  def __init__(self, i2c=None, mode=0, address=0x38):
    if i2c is None:
      raise ValueError('I2C object required.')
    if mode is not (0 and 1):
      raise ValueError('Mode must be either 0 for Celsius or 1 Farenheit')
    self.i2c = i2c
    self.address = address
    self.i2c.writeto(address, AHT10.CMD_INITIALIZE)
    self.readings_raw = bytearray(8)
    self.results_parsed = [0, 0]
    self.mode = mode # 0 for Celsius, 1 for Farenheit
    self.t = None
    self.h = None 
    
  def read_raw(self):
    self.i2c.writeto(self.address, AHT10.CMD_MEASURE)
    time.sleep_ms(AHT10.AHT10_READ_DELAY_MS) # Time it takes for AHT to collect data
    self.readings_raw = self.i2c.readfrom(self.address, 6)
    self.results_parsed[0] = self.readings_raw[1] << 12 | self.readings_raw[2] << 4 | self.readings_raw[3] >> 4
    self.results_parsed[1] = (self.readings_raw[3] & 0x0F) << 16 | self.readings_raw[4] << 8 | self.readings_raw[5]
  
  def get_humidity(self):
    return (self.results_parsed[0] / AHT10.KILOBYTE_CONST) * 100 

  def get_temperature(self):
    t = (self.results_parsed[1] / AHT10.KILOBYTE_CONST) * AHT10.AHT_TEMPERATURE_CONST - AHT10.AHT_TEMPERATURE_OFFSET
    if self.mode is 1:
      t = t * 9/5 + 32
    return round(t,1)

  def set_mode(self, mode):
    if mode is not (0 or 1):
      raise ValueError('Mode must be either 0 for Celsius or 1 Farenheit')
    self.mode = mode

  def dew_point(self):
    h = self.h
    prev_mode = self.mode
    self.mode = 0
    h = (log(h, 10) - 2) / 0.4343 + (17.62 * t) / (243.12 + t)
    return 243.12 * h / (17.62 - h)
  
  def read():
    self.read_raw()
    self.t = self.get_temperature()
    self.h = self.get_humidity()
    return True
  
  @property
  def values(self):
    return self.t, self.h
  
  @property
  def values_dict(self):
    return {'t': self.t, 'h': self.h}
