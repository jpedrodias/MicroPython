# robot1
# WEMOS D1 Mini Board GPIO Map: D8 pull_down, D4 pull_down
# D0=16, D1=5, D2=4, D3=0, D4=2, D5=14, D6=12, D7=13, D8=15
import os, gc, micropython, machine, random, time

class Motor():
  def __init__(self, EN1, EN2):
    if isinstance(EN1, int) and isinstance(EN2, int):
      self.EN1 = machine.Pin(EN1, mode=machine.Pin.OUT, value=0, pull=None)    
      self.EN2 = machine.Pin(EN2, mode=machine.Pin.OUT, value=0, pull=None)
    else:
      raise TypeError('EN1 and EN2 must be integer')
  def forward(self):
    self.EN1.value(1)
    self.EN2.value(0)
  def backward(self):
    self.EN1.value(0)
    self.EN2.value(1)
  def stop(self):
    self.EN1.value(0)
    self.EN2.value(0)
#End Motor

class Robot():
  def __init__(self, M1, M2):
    if isinstance(M1, Motor) and isinstance(M2, Motor):
      self.M1 = M1 # Motor 1
      self.M2 = M2 # Motor 2
    else:
      raise TypeError('M1 and M2 must be a Motor object')
  def stop(self):
    self.M1.stop()
    self.M2.stop()
  def forward(self):
    self.M1.forward()
    self.M2.forward()
  def backward(self):
    self.M1.backward()
    self.M2.backward()
  def turn(self, mode=0):
    if mode == 1:
      self.M1.forward()
    elif mode == 2:
      self.M2.forward()
    else:
      self.M1.forward()
      self.M2.backward()
#End class Robot

motor1 = Motor(13, 15) # D7 = 13, D8 = 15
motor2 = Motor(14, 12) # D5 = 14, D6 = 12
robot = Robot(motor1, motor2)

from sensor_manager import HCSR04
dsensor = HCSR04(trigger=5, echo=4) # D1=5, D4=4

green = machine.Pin(0, machine.Pin.OUT, value=0)  #D3
yellow = machine.Pin(2, machine.Pin.OUT, value=0) #D4
red = machine.Pin(16, machine.Pin.OUT, value=0)   #D0
gc.collect()

DELAY = 1 * 1000
t_start = time.ticks_ms()
while True:
  dsensor.read()
  distance = dsensor.distance_cm
  
  if distance < 5:
    robot.stop()
    green.value(0)
    yellow.value(0)
    red.value(1)
    time.sleep_ms(250)
    robot.backward()
    time.sleep_ms(250)
    robot.stop()
    
  elif distance < 10:
    robot.stop()
    green.value(0)
    yellow.value(1)
    red.value(0)
    time.sleep_ms(250)
    robot.turn( random.getrandbits(2) )
    time.sleep_ms(250)
    robot.stop()
    
  else:
    robot.forward()
    green.value(1)
    yellow.value(0)
    red.value(0)
    
  t_diff = time.ticks_diff(time.ticks_ms(), t_start)
  if t_diff > DELAY:
    print(dsensor.distance_cm)
    t_start = time.ticks_ms()
  time.sleep_ms(50)
