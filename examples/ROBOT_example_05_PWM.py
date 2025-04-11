from machine import Pin, PWM
from time import sleep


class Car:
    def __init__(self, *args):
        self.freq = 1024
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
    
    def set_rotation(self, *pins):
        for motor in self.motors:
            motor.duty_u16(0)
        
        for index in pins:
            motor = self.motors[index]
            motor.duty_u16(2**16)
            motor.duty_u16(self.duty)
        
    def forward(self):
        self.set_rotation(0, 2)

    def backward(self):
        self.set_rotation(1, 3)

    def left(self):
        self.set_rotation(0)

    def right(self):
        self.set_rotation(2)

    def stop(self, side=0):
        self.speed = 0
        for motor in self.motors:
            motor.duty_u16(0)

RUN_PAUSA = True
def pausa_on_click(pin):
    global RUN_PAUSA
    if pin == pausa:
        RUN_PAUSA = not RUN_PAUSA
        print('Status', RUN_PAUSA)
        sleep(0.01)


sensor_esq = Pin(18, Pin.IN)
ssensor_dir = Pin(19, Pin.IN)
pausa = Pin(13, Pin.IN)
pausa.irq(handler=pausa_on_click, trigger=Pin.IRQ_FALLING)
car = Car(15, 14, 17, 16)

car.set_speed(60)
car.stop()

while True:
    if RUN_PAUSA:
        car.stop()
    else:
        
        if sensor_esq.value() and not ssensor_dir.value():
            car.right()
        elif not sensor_esq.value() and sensor_dir.value():
            car.left()
        else:
            car.forward()
#end loop
