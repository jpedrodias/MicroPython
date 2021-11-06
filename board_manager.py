from micropython import const

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

class Clock():
  @property
  def timestamp(self):
    t = time.localtime()
    return '{:04d}-{:02d}-{:02d} {:02d}:{:02d}:{:02d}'.format(*t[:6])
  @staticmethod
  def update():
    try:
      ntptime.settime()
    except:
      return False
    return True
