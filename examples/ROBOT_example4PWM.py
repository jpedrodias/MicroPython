import os, gc, micropython, machine, random, time
from board_manager import D1, D2, D8, D7, D6, D5

from sensor_manager import Sensor_HCSR04
sensor = Sensor_HCSR04(trigger=D1, echo=D2)

from robot_manager import MotorPWM, Robot2WD
motor1 = MotorPWM(D7, D8)
motor2 = MotorPWM(D6, D5)
robot = Robot2WD(motor1, motor2)

motor1.speed(25)
motor2.speed(25)

actions2stop = ((robot.stop, 1),(robot.backward, 0.25),(robot.stop, 1))
actions2avoid = ((robot.stop, 1),(robot.backward, 0.25),(robot.turn, 1),(robot.stop, 1))
actions2move = ((robot.forward, 0.1),(robot.forward, 0.1),)
actions_list = (actions2move, actions2stop, actions2avoid)

ACTION2MOVE = micropython.const(0)
ACTION2STOP = micropython.const(1)
ACTION2AVOID = micropython.const(2)

next_action = ACTION2MOVE
last_action = ACTION2STOP

try:
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
      print('ACTION', next_action)
      for do_action, pause in actions_list[next_action]:
        do_action()
        time.sleep(pause)
    #End if repeat action
    last_action = next_action
except:
  robot.stop()
