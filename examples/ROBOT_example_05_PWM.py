from machine import Pin, PWM
from time import sleep

class Car:
    def __init__(self, *args):
        self.freq = 50
        self.motors_map = args
        
        self.calibration = [0, 0, 0, 0]
        self.motors = []
        for pin in self.motors_map:
            self.motors.append( PWM(Pin(pin, Pin.OUT), freq=self.freq, duty_u16=0) )
        
        for motor in self.motors:
            motor.init()
        
        self.speed = 0
        self.duty = 0

    def set_speed(self, speed):
        """Ajusta a velocidade dos motores."""
        self.speed = speed # 0 e 100
        self.duty = 2 ** 16 * speed // 100
        print(self.duty)
    
    def set_rotation(self, *pins):
        print(pins)
        for motor in self.motors:
            motor.duty_u16(0)
        
        for index in pins:
            motor = self.motors[index]
            motor.duty_u16(self.duty)
        
        
    def move_forward(self):
        self.set_rotation(0, 2)

    def move_backward(self):
        self.set_rotation(1, 3)

    def turn_left(self):
        self.set_rotation(0)

    def turn_right(self):
        self.set_rotation(2)

    def stop(self, side=0):
        self.speed = 0
        for motor in self.motors:
            motor.duty_u16(0)
            

car = Car(15, 14, 17, 16)

car.set_speed(30)
#car.set_rotation(0, 2)
car.turn_right()
sleep(2)
car.stop()

