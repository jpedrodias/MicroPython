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


#https://github.com/m5stack/M5Cloud/blob/master/lib/servo.py
class Servo:
    """
    A simple class for controlling hobby servos.

    Args:
        pin (machine.Pin): The pin where servo is connected. Must support PWM.
        freq (int): The frequency of the signal, in hertz.
        min_us (int): The minimum signal length supported by the servo.
        max_us (int): The maximum signal length supported by the servo.
        angle (int): The angle between the minimum and maximum positions.

    """
    def __init__(self, pin, freq=50, min_us=600, max_us=2400, angle=180):
        self.min_us = min_us
        self.max_us = max_us
        self.us = 0
        self.freq = freq
        self.angle = angle
        
        self.pwm = machine.PWM(machine.Pin(pin,machine.Pin.OUT), freq=freq, duty=0)

    def write_us(self, us):
        """Set the signal to be ``us`` microseconds long. Zero disables it."""
        if us == 0:
            self.pwm.duty(0)
            return
        us = min(self.max_us, max(self.min_us, us))
        duty = us * 1024 * self.freq // 1000000
        self.pwm.duty(duty)

    def write_angle(self, degrees=None, radians=None):
        """Move to the specified angle in ``degrees`` or ``radians``."""
        if degrees is None:
            degrees = math.degrees(radians)
        degrees = degrees % 360
        total_range = self.max_us - self.min_us
        us = self.min_us + total_range * degrees // self.angle
        self.write_us(us)
#End Class Servo
#m1 = Servo(D3)

if __name__ == '__main__':
  pass
