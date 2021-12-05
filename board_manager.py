from micropython import const
import machine
import time

# WEMOS D1 Mini Board GPIO Map: D8 pull_down, D4 pull_down
# D0=16, D1=5, D2=4, D3=0, D4=2, D5=14, D6=12, D7=13, D8=15
D0 = const(16)
D1 = const(5)
D2 = const(4)
D3 = const(0)
D4 = const(2)
D5 = const(14)
D6 = const(12)
D7 = const(13)
D8 = const(15)

class rgb_colors():
    brightness = 50
    RED = (255*brightness, 0, 0)
    GREEN = (0, 255*brightness, 0)
    BLUE = (0, 0, 255*brightness)
    BLACK = (0,0,0)
#End RGB_Colors

class NTPClock():
  @property
  def time(self):
    return time.time()
  @property
  def str_time(self):
    l = self.local
    g = self.gmt
    z = self.zone
    d = '{:04d}-{:02d}-{:02d}'.format(*l[0:3])
    t = '{:02d}:{:02d}:{:02d}'.format(*l[3:6])
    return '{}T{}Z{}'.format(d, t, z)
  @property
  def local(self):
    return time.localtime()
  @property
  def gmt(self):
    return time.gmtime()
  @property
  def zone(self):
    return self.local[4]-self.gmt[4]
  @property
  def timestamp(self):
    return self.str_time
  @staticmethod
  def update():
    try:
      ntptime.settime()
    except:
      return False
    return True
  def __repr__(self):
    return self.str_time

class StatusLED():
  def __init__(self, pin=2):
    self.led = machine.Pin(pin, machine.Pin.OUT)
  def value(self, value):
    self.led.value(value)
  def on(self):
    self.value(1)
  def off(self):
    self.value(0)
  def toggle(self):
    self.led.value(not self.led.value())
    
