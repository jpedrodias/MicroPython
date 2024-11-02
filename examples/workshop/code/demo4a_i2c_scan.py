# filename: demo4a_i2c_scan.py
from machine import Pin, I2C

i2c_sda = Pin(12)
i2c_scl = Pin(13)

# Initialize I2C
i2c = I2C(0,sda=i2c_sda,scl=i2c_scl,freq=100000)

# I2C-Bus-Scan
print('Scan I2C Bus...')
devices = i2c.scan()

# Output scan result 
if len(devices) == 0:
    print('No I2C-device found!')
else:
    print('I2C-devices found:', len(devices))
    for device in devices:
        print('Decimal address:', device, end = '')
        print('| Hexa Address:', hex(device))
