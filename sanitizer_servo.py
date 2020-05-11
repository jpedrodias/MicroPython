#sanitizer
from machine import Pin
from time import sleep
from board_manager import D5
from robot_manager import Servo


class Servo_Spray(Servo):
  def __init__(self, pin, rest=90, press=0, wait=0.3):
    from time import sleep
    self.s = super().__init__(pin)
    self.rest = rest
    self.press = press
    self.wait = wait 
    
  def spray(self):
    self.write_angle(self.press)
    sleep(self.wait)
    servo.write_angle(self.rest)
  
servo = Servo_Spray(D5, 100, 00, 0.3)
sleep(1)
servo.spray()
