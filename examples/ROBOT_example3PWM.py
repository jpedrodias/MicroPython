# robot1
# WEMOS D1 Mini Board GPIO Map: D8 pull_down, D4 pull_down
# D0=16, D1=5, D2=4, D3=0, D4=2, D5=14, D6=12, D7=13, D8=15
import os, gc, micropython, machine, random, time

from sensor_manager import Sensor_HCSR04
sensor = Sensor_HCSR04(trigger=5, echo=4) # D1=5, D2=4

DEBUG = micropython.const(1)

#On the ESP8266 the pins 0, 2, 4, 5, 12, 13, 14 and 15 all support PWM
class MotorPWM():
  def __init__(self, EN1, EN2):
    if not (isinstance(EN1, int) and isinstance(EN2, int)):
      raise TypeError('EN1 and EN2 must be integer')
    self.EN1 = machine.Pin(EN1, mode=machine.Pin.OUT, value=0, pull=None)    
    self.EN2 = machine.Pin(EN2, mode=machine.Pin.OUT, value=0, pull=None)
    self.PWM1 = machine.PWM(self.EN1) # Only one Pin need to do PWM
    self.PWM2 = machine.PWM(self.EN2) # Only one Pin need to do PWM
    self.speed = 20
  
  def stop(self):
    self.PWM1.duty(0)
    self.PWM2.duty(0)
  def forward(self, duty= 200):
    self.PWM2.duty(0)
    self.PWM1.duty(duty)
  def backward(self, duty= 200):
    self.PWM1.duty(0)
    self.PWM2.duty(duty)
#End class MotorPWM

class Robot():
  def __init__(self, M1, M2):
    if isinstance(M1, MotorPWM) and isinstance(M2, MotorPWM):
      self.M1 = M1 # Motor 1
      self.M2 = M2 # Motor 2
    else:
      raise TypeError('M1 and M2 must be a MotorPWM object')
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

motor1 = MotorPWM(12, 14) # D5 = 14, D6 = 12
motor2 = MotorPWM(15, 13) # D7 = 13, D8 = 15

robot = Robot(motor1, motor2)

actions2stop = ((robot.stop, 1),(robot.backward, 0.25),(robot.stop, 1))
actions2avoid = ((robot.stop, 1),(robot.backward, 0.25),(robot.turn, 1),(robot.stop, 1))
actions2move = ((robot.forward, 0.1),(robot.forward, 0.1),)
actions_list = (actions2move, actions2stop, actions2avoid)

ACTION2MOVE = micropython.const(0)
ACTION2STOP = micropython.const(1)
ACTION2AVOID = micropython.const(2)

next_action = ACTION2MOVE
last_action = ACTION2STOP

while 1:
  sensor.read()
  d = sensor.values[0]
  if d < 5:
    next_action = ACTION2STOP
  elif d > 5 and d < 10:
    next_action = ACTION2AVOID
  else:
    next_action = ACTION2MOVE
  #End if distance
  
  if last_action != next_action:
    if DEBUG: print('ACTION', next_action)
    for do_action, pause in actions_list[next_action]:
      do_action()
      time.sleep(pause)
  #End if repeat action
  last_action = next_action
