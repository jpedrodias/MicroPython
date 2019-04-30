# filename: sensor_manager.py
# WEMOS D1 Mini Board GPIO Map: D8 pull_down, D4 pull_down
# D0=16, D1=5, D2=4, D3=0, D4=2, D5=14, D6=12, D7=13, D8=15
import micropython, machine, ustruct, time

#import machine, time
class Sensor_DHT22():
  def __init__(self, pin):
    if not isinstance(pin, int):
      raise TypeError('pin must be integer')
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
    return {'t': self.t, 'h': self.h}
#End of Sensor_DHT22

#import machine, time
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

#import machine, time
class Sensor_BME280():
  def __init__(self, i2c, address=0x76):
    if not isinstance(i2c, machine.I2C):
      raise TypeError('I2C object required.')
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
  def values(self):
    return [self.t, self.h, self.p]
  @property
  def values_dict(self):
    return {'t': self.t, 'h': self.h, 'p': self.p}
#End of Sensor_BME280

#import machine, time
class Sensor_BH1750FVI():
  #adaptation from https://github.com/catdog2/mpy_bh1750fvi_esp8266
  def __init__(self, i2c, address=0x23):
    if not isinstance(i2c, machine.I2C):
      raise TypeError('I2C object required.')
    self.i2c = i2c
    self.address = address
    self.lux = None
  def read(self):
    self.i2c.writeto(self.address, b'\x00') # make sure device is in a clean state
    self.i2c.writeto(self.address, b'\x01') # power up
    self.i2c.writeto(self.address, bytes([0x23])) # set measurement mode
    time.sleep_ms(180)
    raw = self.i2c.readfrom(self.address, 2)
    self.i2c.writeto(self.address, b'\x00') # power down again
    # we must divide the end result by 1.2 to get the lux
    self.lux = ((raw[0] << 24) | (raw[1] << 16)) // 78642
    return self.lux
  @property
  def values(self):
    return [self.lux]
  @property
  def values_dict(self):
    return {'lux': self.lux}
#End of Sensor_BH1750FVI

class Sensor_DS18B20():
  def __init__(self, pin):
    if not isinstance(pin, int):
      raise TypeError('pin must be integer')
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
      temps_dict['t{}'.format(i)] = value
    return temps_dict
#End of Sensor_DS18B20

#import machine, time
class Sensor_BUTTONS():
  def __init__(self, pins):
    if not isinstance(pins, list):
      raise TypeError('pins must be a list of pins')
    self.buttons = []
    for pin in pins:
      if not isinstance(pin, int):
        raise TypeError('pin must be a integer')
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
      buttons_dict['b{}'.format(i)] = self.states[i]
      buttons_dict['_b{}'.format(i)] = self.previews_states[i]
    return buttons_dict
#End Sensor_BUTTONS

#import machine, time
class Sensor_HCSR04():
  def __init__(self, trigger, echo, echo_timeout_us=500000):
    if isinstance(trigger, int) and isinstance(echo, int):
      self.trigger = machine.Pin(trigger, mode=machine.Pin.OUT, pull=None)    
      self.echo = machine.Pin(echo, mode=machine.Pin.IN, pull=None)
    else:
      raise TypeError('trigger and echo must be integer')
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
  @property
  def values(self):
    return [self.distance_cm]
  @property
  def values_dict(self):
    return {'d': self.distance_cm}
#End of HCSR04

#import machine, time
class PhotoGate():  
  def __init__(self, pin, mode=True):
    if not isinstance(pin, int):
      raise TypeError('pin must be integer')
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


#import micropython, machine, ustruct, time
class TimeoutError(RuntimeError):
  pass
class VL53L0X:
  _IO_TIMEOUT = micropython.const(1000)
  _SYSRANGE_START = micropython.const(0x00)
  _EXTSUP_HV = micropython.const(0x89)
  _MSRC_CONFIG = micropython.const(0x60)
  _FINAL_RATE_RTN_LIMIT = micropython.const(0x44)
  _SYSTEM_SEQUENCE = micropython.const(0x01)
  _SPAD_REF_START = micropython.const(0x4f)
  _SPAD_ENABLES = micropython.const(0xb0)
  _REF_EN_START_SELECT = micropython.const(0xb6)
  _SPAD_NUM_REQUESTED = micropython.const(0x4e)
  _INTERRUPT_GPIO = micropython.const(0x0a)
  _INTERRUPT_CLEAR = micropython.const(0x0b)
  _GPIO_MUX_ACTIVE_HIGH = micropython.const(0x84)
  _RESULT_INTERRUPT_STATUS = micropython.const(0x13)
  _RESULT_RANGE_STATUS = micropython.const(0x14)
  _OSC_CALIBRATE = micropython.const(0xf8)
  _MEASURE_PERIOD = micropython.const(0x04)

  def __init__(self, i2c, address=0x29):
    if isinstance(i2c, str):           # Non-pyb targets may use other than X or Y
      self.i2c = I2C(i2c)
    elif isinstance(i2c, int):         # WiPY targets
      self.i2c = I2C(i2c)
    elif hasattr(i2c, 'readfrom'):     # Soft or hard I2C instance. See issue #3097
      self.i2c = i2c
    else:
      raise ValueError("Invalid I2C instance")

    self.address = address
    self.init()
    self._started = False

  def _registers(self, register, values=None, struct='B'):
    if values is None:
      size = ustruct.calcsize(struct)
      data = self.i2c.readfrom_mem(self.address, register, size)
      values = ustruct.unpack(struct, data)
      return values
    data = ustruct.pack(struct, *values)
    self.i2c.writeto_mem(self.address, register, data)

  def _register(self, register, value=None, struct='B'):
    if value is None:
      return self._registers(register, struct=struct)[0]
    self._registers(register, (value,), struct=struct)

  def _flag(self, register=0x00, bit=0, value=None):
    data = self._register(register)
    mask = 1 << bit
    if value is None:
      return bool(data & mask)
    elif value:
      data |= mask
    else:
      data &= ~mask
    self._register(register, data)

  def _config(self, *config):
    for register, value in config:
      self._register(register, value)
  
  def init(self, power2v8=True):
    self._flag(self._EXTSUP_HV, 0, power2v8)
    # I2C standard mode
    self._config((0x88, 0x00),(0x80, 0x01),(0xff, 0x01),(0x00, 0x00),)
    self._stop_variable = self._register(0x91)
    self._config((0x00, 0x01),(0xff, 0x00),(0x80, 0x00),)
    # disable signal_rate_msrc and signal_rate_pre_range limit checks
    self._flag(self._MSRC_CONFIG, 1, True)
    self._flag(self._MSRC_CONFIG, 4, True)
    # rate_limit = 0.25
    self._register(self._FINAL_RATE_RTN_LIMIT, int(0.25 * (1 << 7)),struct='>H')
    self._register(self._SYSTEM_SEQUENCE, 0xff)
    spad_count, is_aperture = self._spad_info()
    spad_map = bytearray(self._registers(self._SPAD_ENABLES, struct='6B'))
    # set reference spads
    self._config(
      (0xff, 0x01),(self._SPAD_REF_START, 0x00),(self._SPAD_NUM_REQUESTED, 0x2c),
      (0xff, 0x00),(self._REF_EN_START_SELECT, 0xb4),)
    spads_enabled = 0
    for i in range(48):
      if i < 12 and is_aperture or spads_enabled >= spad_count:
        spad_map[i // 8] &= ~(1 << (i >> 2))
      elif spad_map[i // 8] & (1 << (i >> 2)):
        spads_enabled += 1
    self._registers(self._SPAD_ENABLES, spad_map, struct='6B')
    self._config(
      (0xff, 0x01),(0x00, 0x00),(0xff, 0x00),(0x09, 0x00),
      (0x10, 0x00),(0x11, 0x00),(0x24, 0x01),(0x25, 0xFF),
      (0x75, 0x00),(0xFF, 0x01),(0x4E, 0x2C),(0x48, 0x00),
      (0x30, 0x20),(0xFF, 0x00),(0x30, 0x09),(0x54, 0x00),
      (0x31, 0x04),(0x32, 0x03),(0x40, 0x83),(0x46, 0x25),
      (0x60, 0x00),(0x27, 0x00),(0x50, 0x06),(0x51, 0x00),
      (0x52, 0x96),(0x56, 0x08),(0x57, 0x30),(0x61, 0x00),
      (0x62, 0x00),(0x64, 0x00),(0x65, 0x00),(0x66, 0xA0),
      (0xFF, 0x01),(0x22, 0x32),(0x47, 0x14),(0x49, 0xFF),
      (0x4A, 0x00),(0xFF, 0x00),(0x7A, 0x0A),(0x7B, 0x00),
      (0x78, 0x21),(0xFF, 0x01),(0x23, 0x34),(0x42, 0x00),
      (0x44, 0xFF),(0x45, 0x26),(0x46, 0x05),(0x40, 0x40),
      (0x0E, 0x06),(0x20, 0x1A),(0x43, 0x40),(0xFF, 0x00),
      (0x34, 0x03),(0x35, 0x44),(0xFF, 0x01),(0x31, 0x04),
      (0x4B, 0x09),(0x4C, 0x05),(0x4D, 0x04),(0xFF, 0x00),
      (0x44, 0x00),(0x45, 0x20),(0x47, 0x08),(0x48, 0x28),
      (0x67, 0x00),(0x70, 0x04),(0x71, 0x01),(0x72, 0xFE),
      (0x76, 0x00),(0x77, 0x00),(0xFF, 0x01),(0x0D, 0x01),
      (0xFF, 0x00),(0x80, 0x01),(0x01, 0xF8),(0xFF, 0x01),
      (0x8E, 0x01),(0x00, 0x01),(0xFF, 0x00),(0x80, 0x00),)

    self._register(self._INTERRUPT_GPIO, 0x04)
    self._flag(self._GPIO_MUX_ACTIVE_HIGH, 4, False)
    self._register(self._INTERRUPT_CLEAR, 0x01)
    # XXX Need to implement this.
    #budget = self._timing_budget()
    #self._register(_SYSTEM_SEQUENCE, 0xe8)
    #self._timing_budget(budget)
    self._register(self._SYSTEM_SEQUENCE, 0x01)
    self._calibrate(0x40)
    self._register(self._SYSTEM_SEQUENCE, 0x02)
    self._calibrate(0x00)
    self._register(self._SYSTEM_SEQUENCE, 0xe8)

  def _spad_info(self):
    self._config(
      (0x80, 0x01),(0xff, 0x01),(0x00, 0x00),(0xff, 0x06),)
    self._flag(0x83, 3, True)
    self._config((0xff, 0x07),(0x81, 0x01),(0x80, 0x01),(0x94, 0x6b),(0x83, 0x00),)
    for timeout in range(self._IO_TIMEOUT):
      if self._register(0x83):
        break
      time.sleep_ms(1)
    else:
      raise TimeoutError()
    self._config((0x83, 0x01),)
    value = self._register(0x92)
    self._config((0x81, 0x00),(0xff, 0x06),)
    self._flag(0x83, 3, False)
    self._config((0xff, 0x01),(0x00, 0x01),(0xff, 0x00),(0x80, 0x00),)
    count = value & 0x7f
    is_aperture = bool(value & 0b10000000)
    return count, is_aperture

  def _calibrate(self, vhv_init_byte):
    self._register(self._SYSRANGE_START, 0x01 | vhv_init_byte)
    for timeout in range(self._IO_TIMEOUT):
      if self._register(self._RESULT_INTERRUPT_STATUS) & 0x07:
        break
      time.sleep_ms(1)
    else:
      raise TimeoutError()
    self._register(self._INTERRUPT_CLEAR, 0x01)
    self._register(self._SYSRANGE_START, 0x00)

  def start(self, period=0):
    self._config(
      (0x80, 0x01),(0xFF, 0x01),(0x00, 0x00),(0x91, self._stop_variable),
      (0x00, 0x01),(0xFF, 0x00),(0x80, 0x00),)
    if period:
      oscilator = self._register(self._OSC_CALIBRATE, struct='>H')
      if oscilator:
        period *= oscilator
      self._register(self._MEASURE_PERIOD, period, struct='>H')
      self._register(self._SYSRANGE_START, 0x04)
    else:
      self._register(self._SYSRANGE_START, 0x02)
    self._started = True

  def stop(self):
    self._register(self._SYSRANGE_START, 0x01)
    self._config(
      (0xFF, 0x01),(0x00, 0x00),(0x91, self._stop_variable),
      (0x00, 0x01),(0xFF, 0x00),)
    self._started = False

  def read(self):
    if not self._started:
      self._config(
        (0x80, 0x01),(0xFF, 0x01),(0x00, 0x00),(0x91, self._stop_variable),
        (0x00, 0x01),(0xFF, 0x00),(0x80, 0x00),(self._SYSRANGE_START, 0x01),)
    for timeout in range(self._IO_TIMEOUT):
      if not self._register(self._SYSRANGE_START) & 0x01:
        break
      time.sleep_ms(1)
    else:
      raise TimeoutError()
    for timeout in range(self._IO_TIMEOUT):
      if self._register(self._RESULT_INTERRUPT_STATUS) & 0x07:
        break
      time.sleep_ms(1)
    else:
      raise TimeoutError()
    value = self._register(self._RESULT_RANGE_STATUS + 10, struct='>H')
    self._register(self._INTERRUPT_CLEAR, 0x01)
    return value
#End class VL53L0X

class Sensor_VL53L0X(VL53L0X):
  def __init__(self,  *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.value = None
  def read(self):
    self.value = super().read()
    return self.value
  @property
  def values(self):
    return [self.value]
  @property
  def values_dict(self):
    return {'d': self.value}
#End class Sensor_VL53L0X

if __name__ == '__main__':
  print('Sensor manager')

#End of file
