# filename: sensors/sensor_sht30.py
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
