# filename: sensor/uhcsr04.py
# WEMOS D1 Mini Board GPIO Map: D8 pull_down, D4 pull_down
# D0=16, D1=5, D2=4, D3=0, D4=2, D5=14, D6=12, D7=13, D8=15
import machine, time

class HCSR04():
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
