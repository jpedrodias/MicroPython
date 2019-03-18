import micropython, machine
import time # sleep_us, ticks_us, ticks_diff

DEBUG = micropython.const(1) # Change from 1 debug mode to 0 production mode
DEBUG_TIME = micropython.const(10) # Run in debug mode for this amount of seconds
DELAY_TIME = micropython.const(1)  # Delay between loops
print('PhotoGate in MicroPython - v0.1')

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
  def show_ms(self):
    return round(time.ticks_diff(self.t_end, self.t_ini) / 1000, 3)
  def show_us(self):
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


g1 = PhotoGate(14, mode=1) # mode = 1 | 0 
while True:
  g1.read()
  if g1.event_change_to(1):
    g1.start_time()
  if g1.event_change_to(0):
    g1.stop_time()
    print(g1.show_ms(), 'ms')
  g1.store()
  time.sleep_us(DELAY_TIME)
#End while loops


#if __name__ == '__main__':
#  main()
