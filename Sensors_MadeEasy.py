# Sensors_MadeEasy.py
from time import sleep, sleep_ms

class Sensor_DHT22():
  def __init__(self, PinObject):
    from dht import DHT22
    self.sensor = DHT22(PinObject)
    sleep( 1 ) # delay to stabilize sensor
    self.t = None
    self.h = None
  def read(self):
    self.sensor.measure()
    self.t, self.h = self.sensor.temperature(), self.sensor.humidity()
    self.t, self.h = round(self.t,1), round(self.h,1)
    return [self.t, self.h]
  @property
  def values_dict(self):
    return {"t": self.t, "h": self.h}
  @property
  def values(self):
    return [self.t, self.h]

class Sensor_DHT11():
  def __init__(self, PinObject):
    from dht import DHT11 as DHT
    self.sensor = DHT11(PinObject)
    sleep(1) # delay to stabilize sensor
    self.t = None
    self.h = None
  def read(self):
    self.sensor.measure()
    self.t, self.h = self.sensor.temperature(), self.sensor.humidity()
    self.t, self.h = round(self.t,1), round(self.h,1)
    return [self.t, self.h]
  @property
  def values_dict(self):
    return {"t": self.t, "h": self.h}
  @property
  def values(self):
    return [self.t, self.h]
        
class Sensor_BME280():
  def __init__(self, i2c, address=0x76):
    from libs import bme280 as bme280
    self.bme = bme280.BME280(i2c=i2c,address=address)
    self.t = None
    self.h = None
    self.p = None
  def read(self):
    self.t, self.p, self.h = self.bme.values
    self.t = round(self.t,1)
    self.p = round(self.p,2)
    self.h = round(self.h,1)
    return [self.t, self.h, self.p]
  @property
  def values_dict(self):
    return {"t": self.t, "h": self.h, "p": self.p}
  @property
  def values(self):
    return [self.t, self.h, self.p]

class Sensor_DS18B20():
  def __init__(self, PinObject):
    from onewire import OneWire
    from ds18x20 import DS18X20
    ow = OneWire(PinObject) 
    ow.scan()
    ow.reset()
    self.ds18b20 = DS18X20(ow)
    self.roms = self.ds18b20.scan()
    self.temps = [None for rom in self.roms]
  def read(self):
    self.ds18b20.convert_temp()
    sleep_ms(750)
    for i, rom in enumerate(self.roms):
      t = self.ds18b20.read_temp(rom)
      self.temps[i] = round(t, 1)
    return self.temps
  @property
  def values_dict(self):
    temps_dict = {}
    for i, value in enumerate(self.temps):
      temps_dict["t{}".format(i)] = value
    return temps_dict
  @property
  def values(self):
    return self.temps

class Sensor_BUTTONS():
  def __init__(self, PinObjects):
    if type(PinObjects) != type([]):
      raise TypeError("Must be list of Pins")
    self.buttons = PinObjects
    self.states = [button.value() for button in self.buttons]
    self.previews_states = [value for value in self.states]
    self.new_event = False
  def read(self):
    self.new_event = False
    for i, button in enumerate(self.buttons):
      self.previews_states[i] = self.states[i]
      self.states[i] = button.value()
      self.new_event = self.new_event or (self.states[i] != self.previews_states[i])
    return self.states
  @property
  def values_dict(self):
    buttons_dict = {}
    for i in range(len(self.states)):
      buttons_dict["b{}".format(i)] = self.states[i]
      buttons_dict["_b{}".format(i)] = self.previews_states[i]
    return buttons_dict
  @property
  def values(self):
    return self.states

if __name__ == "__main__":
    from machine import Pin
    from time import sleep
    #from Sensors_MadeEasy import Sensor_BUTTONS
    sensor = Sensor_BUTTONS([Pin(13, Pin.IN, Pin.PULL_UP)]) # Pin 13 = D7
    for i in range(11):
        sensor.read()
        print(sensor.new_event)
        sleep(1)