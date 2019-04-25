# filename: sensors/sensor_photogate.py
# WEMOS D1 Mini Board GPIO Map: D8 pull_down, D4 pull_down
# D0=16, D1=5, D2=4, D3=0, D4=2, D5=14, D6=12, D7=13, D8=15
import machine, time

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
