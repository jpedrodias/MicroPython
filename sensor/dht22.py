# filename: sensor/dht22r.py
# WEMOS D1 Mini Board GPIO Map: D8 pull_down, D4 pull_down
# D0=16, D1=5, D2=4, D3=0, D4=2, D5=14, D6=12, D7=13, D8=15
import machine, time

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
