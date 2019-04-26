# robot1
# WEMOS D1 Mini Board GPIO Map: D8 pull_down, D4 pull_down
# D0=16, D1=5, D2=4, D3=0, D4=2, D5=14, D6=12, D7=13, D8=15
import os, gc, micropython, machine, random, time

from sensor_manager import Sensor_HCSR04
usonic = Sensor_HCSR04(trigger=5, echo=4) # D1=5, D2=4

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

motor1 = Motor(14, 16) # D0 = 16, D5 = 14
motor2 = Motor(13, 12) # D6 = 12, D7 = 13
robot = Robot(motor1, motor2)

stop = (
  (robot.stop, 1),
  (robot.backward, 0.25),
  (robot.stop, 1)
)

avoid = (
  (robot.stop, 1),
  (robot.backward, 0.25),
  (robot.turn, 1),
  (robot.stop, 1)
)
move = (
  (robot.forward, 0.1),
  (robot.forward, 0.1),
)

actions = (move, stop, avoid)
ACTION_MOVE = 0
ACTION_STOP = 1
ACTION_AVOID = 2

ACTION = 0

try:
  while 1:
    usonic.read()
    d = usonic.values[0]
    if d < 5:
      ACTION = ACTION_STOP
    elif d > 5 and d < 10:
      ACTION = ACTION_AVOID
    else:
      ACTION = ACTION_MOVE
    
    for action, delay in actions[ACTION]:
      action()
      time.sleep(delay)
except:
  robot.stop()
