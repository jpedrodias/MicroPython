import machine, time

class MotorDC():
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

class MotorPWM():
  def __init__(self, EN1, EN2):
    if not (isinstance(EN1, int) and isinstance(EN2, int)):
      raise TypeError('EN1 and EN2 must be integer')
    self.EN1 = machine.Pin(EN1, mode=machine.Pin.OUT, value=0, pull=None)    
    self.EN2 = machine.Pin(EN2, mode=machine.Pin.OUT, value=0, pull=None)
    self.PWM1 = machine.PWM(self.EN1, freq=500) 
    self.PWM2 = machine.PWM(self.EN2, freq=500)
    self._speed = 20
    self._duty = 204
  def speed(self, value=None):
    if not value:
      return self._speed
    self._speed = (value % 101)
    self._duty = self._speed * 1024 // 100
    return self._duty, self._speed
  def stop(self):
    self.PWM1.duty(0)
    self.PWM2.duty(0)
  def forward(self):
    self.PWM2.duty(0)
    self.PWM1.duty(self._duty)
  def backward(self):
    self.PWM1.duty(0)
    self.PWM2.duty(self._duty)
#End class MotorPWM

class Robot2WD():
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

if __name__ == '__main__':
  from board_manager import D5, D6, D7, D8
  motor1 = MotorPWM(D7, D8)
  motor2 = MotorPWM(D6, D5)
  motor1.speed(20)
  motor2.speed(20)
  motor1.forward()
  motor2.forward()
  time.sleep(1)
  motor1.stop()
  motor2.stop()
