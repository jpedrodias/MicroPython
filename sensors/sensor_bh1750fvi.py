# filename: sensors/sensor_bh1750fvi.py
# WEMOS D1 Mini Board GPIO Map: D8 pull_down, D4 pull_down
# D0=16, D1=5, D2=4, D3=0, D4=2, D5=14, D6=12, D7=13, D8=15
import machine, time

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
