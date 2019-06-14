import os, gc, micropython, machine, random, time
from board_manager import *
from sensor_manager import Sensor_HCSR04
from robot_manager import MotorPWM, Robot2WD

sensor = Sensor_HCSR04(trigger=D1, echo=D2)
motorR = MotorPWM(D7, D8)
motorL = MotorPWM(D6, D5)
robot = Robot2WD(motorR, motorL)

motorR.speed(42)
motorL.speed(40)

def random_turn():
  robot.turn(random.getrandbits(3))

robot_move = ((robot.forward, 0.1),)
robot_stop = ((robot.stop, 1),(robot.backward, 0.25), (robot.stop, 0.1))
robot_avoid = ((robot.stop, 1),(robot.backward, 0.25),(random_turn, 0.5),(robot.stop, 1))
robot_actions = (robot_move, robot_stop, robot_avoid)

ROBOT_MOVE = micropython.const(0) # referes to robot_actions index
ROBOT_STOP = micropython.const(1)
ROBOT_AVOID = micropython.const(2)

next_action = ROBOT_MOVE
last_action = ROBOT_STOP
time.sleep(5) # time to Ctrl+C into REPL

try:
  while 1:
    sensor.read()
    d = sensor.distance_cm
    if d < 5:
      next_action = ROBOT_STOP
    elif d > 5 and d < 10:
      next_action = ROBOT_AVOID
    else:
      next_action = ROBOT_MOVE
    #End if distance
    
    if last_action != next_action:
      print('ACTION', next_action)
      for do_action, pause in robot_actions[next_action]:
        do_action()
        time.sleep(pause)
    #End if repeat action
    time.sleep_ms(250)
    last_action = next_action
except:
  robot.stop()
