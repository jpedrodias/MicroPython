# filename: sensor/ubme280.py
# WEMOS D1 Mini Board GPIO Map: D8 pull_down, D4 pull_down
# D0=16, D1=5, D2=4, D3=0, D4=2, D5=14, D6=12, D7=13, D8=15
import machine, time
class Sensor_BME280():
  def __init__(self, i2c, address=0x76):
    if not isinstance(i2c, machine.I2C):
      raise TypeError('I2C object required.')
      
    from bme280_ import BME280
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
