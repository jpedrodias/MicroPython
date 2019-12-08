# filename: sensor_manager.py
import micropython, machine, ustruct, time, math

# from https://github.com/robert-hh/BMP085_BMP180
class Sensor_BMP085():
  def __init__(self, i2c, address=0x77):
    if not isinstance(i2c, machine.I2C):
      raise TypeError("I2C object required.")
    from bmp085 import BMP085
    self.bmp = BMP085(i2c=i2c)
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
        super().__init__(i2c, address)
#End of Sensor_BMP180
