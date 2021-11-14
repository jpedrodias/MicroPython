# filename: sensor_manager.py -- version 2021/10/24
import micropython, machine, ustruct, time

class Sensor_BUTTONS():
  def __init__(self, pins):
    if not isinstance(pins, list):
      raise TypeError("pins must be a list of pins")
    self.buttons = []
    for pin in pins:
      if not isinstance(pin, int):
        raise TypeError("pin must be a integer")
      self.buttons.append(machine.Pin(pin, machine.Pin.OUT))
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
  def values(self):
    return self.states
  @property
  def values_dict(self):
    buttons_dict = {}
    for i in range(len(self.states)):
      buttons_dict["b{}".format(i)] = self.states[i]
      buttons_dict["_b{}".format(i)] = self.previews_states[i]
    return buttons_dict
#End Sensor_BUTTONS

class PhotoGate():  
  def __init__(self, pin, mode=True):
    if not isinstance(pin, int):
      raise TypeError("pin must be integer")
    self.pin =  machine.Pin(pin, machine.Pin.IN)
    self.mode = mode
    self.now = mode
    self.last = mode
    self.t_ini = None
    self.t_end = None
  def start_time(self):
    self.t_ini = time.ticks_us()
  def stop_time(self):
    self.t_end = time.ticks_us()
  @property
  def millis(self):
    return round(time.ticks_diff(self.t_end, self.t_ini) / 1000, 3)
  @property
  def micros(self):
    return round(time.ticks_diff(self.t_end, self.t_ini), 0)
  def event_change_to(self, direction=0):
    if direction == self.mode:
      return self.last - self.now == 1
    else:
      return self.now - self.last == 1
  def read(self):
    self.now = self.pin.value()
  def store(self):
    self.last = self.now # store value in the end of the loop
  def value(self):
    return self.now
#End class PhotoGate

class PhotoGateData(PhotoGate):
  BSIZE = micropython.const(8)
  def __init__(self, pin, mode=True):
    PhotoGate.__init__(self, pin, mode=mode)
    self.data = list(0.0 for i in range(self.BSIZE))
    self.cl = 0 # Current Line
  def storedata(self):
    self.data[self.cl] = self.micros
    self.cl = (self.cl + 1) % self.BSIZE  # Virtual Index
  @property
  def ordered(self):
    return list(self.data[(i + self.cl) % self.BSIZE] for i in range(self.BSIZE))
#End class PhotoGateData

class Sensor_SHT30():
  def __init__(self, i2c, address=0x45):
    if not isinstance(i2c, machine.I2C):
      raise TypeError('I2C object required.')
    from sht30 import SHT30
    self.sht = SHT30(i2c=i2c,address=address)
    self.t = None
    self.h = None
  def read(self):
    self.t, self.h = self.sht.measure()
    self.t = round(self.t,1)
    self.h = round(self.h,1)
    return [self.t, self.h]
  @property
  def values(self):
    return [self.t, self.h]
  @property
  def values_dict(self):
    return {'t': self.t, 'h': self.h}
#End of Sensor_SHT30

class Sensor_DS18B20():
  def __init__(self, pin):
    if not isinstance(pin, int):
      raise TypeError("pin must be integer")
    from onewire import OneWire
    from ds18x20 import DS18X20
    ow = OneWire(machine.Pin(pin)) 
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
  def values(self):
    return self.temps
  @property
  def values_dict(self):
    temps_dict = {}
    for i, value in enumerate(self.temps):
      temps_dict["t{}".format(i)] = value
    return temps_dict
#End of Sensor_DS18B20

class Sensor_DHT11():
  def __init__(self, pin):
    if not isinstance(pin, int):
      raise TypeError('pin must be integer')
    from dht import DHT11
    self.sensor = DHT11(machine.Pin(pin))
    time.sleep(1) # some delay to stabilize sensor
    self.t = None
    self.h = None
  def read(self):
    self.sensor.measure()
    self.t, self.h = self.sensor.temperature(), self.sensor.humidity()
    self.t, self.h = round(self.t,1), round(self.h,1)
    return [self.t, self.h]
  @property
  def values(self):
    return [self.t, self.h]
  @property
  def values_dict(self):
    return {'t': self.t, 'h': self.h}
#End of Sensor_DHT11

class Sensor_DHT22():
  def __init__(self, pin):
    if not isinstance(pin, int):
      raise TypeError("pin must be integer")
    from dht import DHT22
    self.sensor = DHT22(machine.Pin(pin))
    time.sleep( 1 ) # some delay to stabilize sensor
    self.t = None
    self.h = None
  def read(self):
    self.sensor.measure()
    self.t, self.h = self.sensor.temperature(), self.sensor.humidity()
    self.t, self.h = round(self.t,1), round(self.h,1)
    return [self.t, self.h]
  @property
  def values(self):
    return [self.t, self.h]
  @property
  def values_dict(self):
    return {"t": self.t, "h": self.h}
#End of Sensor_DHT22

# from https://github.com/robert-hh/BMP085_BMP180
class Sensor_BMP085():
  def __init__(self, i2c, address=0x77):
    if not isinstance(i2c, machine.I2C):
      raise TypeError("I2C object required.")
    from bmp085 import BMP085
    self.bmp = BMP085(i2c=i2c, address=address)
    self.t = None
    self.p = None
    self.a = None
    self.bmp.sealevel = 101325
  def read(self):
    self.t = self.bmp.temperature 
    self.p = self.bmp.pressure
    self.a = self.bmp.altitude
    self.t = round(self.t,1)
    self.p = round(self.p,2)
    self.a = round(self.a,1)
    return [self.t, self.p, self.a]
  @property
  def values(self):
    return [self.t, self.p, self.a]
  @property
  def values_dict(self):
    return {"t": self.t, "p": self.p, "a": self.a}
#End of Sensor_BMP085

class Sensor_BMP180(Sensor_BMP085):
    def __init__(self, i2c=None, address=0x77):
        super().__init__(i2c=i2c, address=address)
#End of Sensor_BMP180

class Sensor_BME280():
  def __init__(self, i2c, address=0x76):
    if not isinstance(i2c, machine.I2C):
      raise TypeError("I2C object required.")
    from bme280 import BME280
    self.bme = BME280(i2c=i2c, address=address)
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
  def values(self):
    return [self.t, self.h, self.p]
  @property
  def values_dict(self):
    return {"t": self.t, "h": self.h, "p": self.p}
#End of Sensor_BME280

#adaptation from https://github.com/catdog2/mpy_bh1750fvi_esp8266
class Sensor_BH1750FVI():
  def __init__(self, i2c, address=0x23):
    if not isinstance(i2c, machine.I2C):
      raise TypeError("I2C object required.")
    self.i2c = i2c
    self.address = address
    self.lux = None
  def read(self):
    self.i2c.writeto(self.address, b"\x00")
    self.i2c.writeto(self.address, b"\x01")
    self.i2c.writeto(self.address, bytes([0x23]))
    time.sleep_ms(180)
    raw = self.i2c.readfrom(self.address, 2)
    self.i2c.writeto(self.address, b"\x00") 
    self.lux = ((raw[0] << 24) | (raw[1] << 16)) // 78642
    return self.lux
  @property
  def values(self):
    return [self.lux]
  @property
  def values_dict(self):
    return {"lux": self.lux}
#End of Sensor_BH1750FVI

class Sensor_BH1750(Sensor_BH1750FVI):
    def __init__(self, i2c=None, address=0x77):
        super().__init__(i2c, address)
#End of Sensor_BH1750

class Sensor_HCSR04():
  def __init__(self, trigger, echo, echo_timeout_us=500000):
    if isinstance(trigger, int) and isinstance(echo, int):
      self.trigger = machine.Pin(trigger, mode=machine.Pin.OUT, pull=None)    
      self.echo = machine.Pin(echo, mode=machine.Pin.IN, pull=None)
    else:
      raise TypeError("trigger and echo must be integer")
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
        raise OSError("Out of range")
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
  @property
  def values(self):
    return [self.distance_cm]
  @property
  def values_dict(self):
    return {"d": self.distance_cm}
#End of HCSR04

class Sensor_VL53L0X():
  def __init__(self, i2c, address=0x76):
    if not isinstance(i2c, machine.I2C):
      raise TypeError("I2C object required.")
    from vl53l0x import VL53L0X
    self.sensor = VL53L0X(i2c=i2c, address=address)
    self.d = None
  def read(self):
    self.d = self.sensor.read()
    return self.d
  @property
  def values(self):
    return [self.d]
  @property
  def values_dict(self):
    return {"d": self.d}
#End class Sensor_VL53L0X
  
if __name__ == '__main__':
  print('Sensor manager')
#End of file
