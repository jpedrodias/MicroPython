# filename: sensors_manager.py
import machine
import time

class Sensor_DHT22():
  def __init__(self, dht22_pin):
    from dht import DHT22
    pin = machine.Pin(dht22_pin)
    self.sensor = DHT22(pin)
    time.sleep( 1 ) # delay to stabilize sensor
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
  def __init__(self, dht11_pin):
    from dht import DHT11
    pin = machine.Pin(dht11_pin)
    self.sensor = DHT11(pin)
    time.sleep(1) # delay to stabilize sensor
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
    from bme280 import BME280
    self.bme = BME280(i2c=i2c,address=address)
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


class Sensor_BH1750FVI():
  #adaptation from https://github.com/catdog2/mpy_bh1750fvi_esp8266
  def __init__(self, i2c, address=0x23):
    self.i2c = i2c
    self.address = address
    self.lux = None
  def read(self):
    self.i2c.writeto(self.address, b"\x00")  # make sure device is in a clean state
    self.i2c.writeto(self.address, b"\x01")  # power up
    self.i2c.writeto(self.address, bytes([0x23]))  # set measurement mode
    time.sleep_ms(180)
    raw = self.i2c.readfrom(self.address, 2)
    self.i2c.writeto(self.address, b"\x00")  # power down again
    # we must divide the end result by 1.2 to get the lux
    self.lux = ((raw[0] << 24) | (raw[1] << 16)) // 78642
    return self.lux
  @property
  def values_dict(self):
    return {"lux": self.lux}
  @property
  def values(self):
    return [self.lux]
    
class Sensor_DS18B20():
  def __init__(self, ds18b20_pin):
    from onewire import OneWire
    from ds18x20 import DS18X20
    pin = machine.Pin(ds18b20_pin)
    ow = OneWire(pin) 
    ow.scan()
    ow.reset()
    self.ds18b20 = DS18X20(ow)
    self.roms = self.ds18b20.scan()
    self.temps = [None for rom in self.roms]
  def read(self):
    self.ds18b20.convert_temp()
    time.sleep_ms(750)
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

class HCSR04():
  def __init__(self, trigger_pin, echo_pin, echo_timeout_us=500000):
    self.trigger = machine.Pin(trigger_pin, mode=machine.Pin.OUT, pull=None)
    self.echo = machine.Pin(echo_pin, mode=machine.Pin.IN, pull=None)
    self.echo_timeout_us = echo_timeout_us
    self.trigger.value(0)
    self.pulse_time = None
  def _send_pulse_and_wait(self):
    self.trigger.value(0)
    time.sleep_us(5)
    self.trigger.value(1)
    time.sleep_us(10)
    self.trigger.value(0)
    try:
      pulse_time = machine.time_pulse_us(self.echo, 1, self.echo_timeout_us)
      return pulse_time
    except OSError as ex:
      if ex.args[0] == 110: # 110 = ETIMEDOUT
        raise OSError('Out of range')
      raise ex
  def read(self):
    self.pulse_time = self._send_pulse_and_wait()
    return self.pulse_time
  @property
  def distance_mm(self):
    if self.pulse_time:
      return self.pulse_time * 100 // 582
    else:
      return None
  @property
  def distance_cm(self):
    if self.pulse_time:
      return (self.pulse_time / 2) / 29.1
    else:
      return None
  
if __name__ == "__main__":
  print('Sensor manager')
  
