# MicroPython
Some tools to help when using MicroPython (tested on wemos d1 mini - esp8266)

<ul>
  <li>how to use wlan manager</li>
  <li>how to use mqtt manager</li>
  <li>how to use sensors manager</li>
</ul>



# WLAN Manager :: Setup
Send wlan_manager.py to board using:
```
ampy -p /dev/ttyUSB0 put wlan_manager.py
```

The first time you need to run the `setup()` function. This function will creat the file wlan_manager.json to store SSID and password
```
from wlan_manager import WLAN_Manager
wlan_client = WLAN_Manager()
wlan_client.setup() # wlan_manager.json file to store SSID and password
wlan_client.setup('HOME', 'password', append=False) # overwrite the file and store this settings
wlan_client.setup('WORK', 'password', append=True)  # appends this settings to the file
wlan_client.start()
```

# WLAN Manager :: main loop example
```
from time import sleep
from gc import collect

# Connection to Wireless
from wlan_manager import WLAN_Manager
wlan_client = WLAN_Manager()
sleep(1)
Done = False
while not Done:
  wlan_client.start()
  Done = wlan_client.check()
  sleep(1)
del(Done)
collect()
```

# MQTT Manager :: Setup
Send mqtt_manager.py and mqtt_manager.json (change here your mqtt setting first) to board using:
```
ampy -p /dev/ttyUSB0 put mqtt_manager.py
ampy -p /dev/ttyUSB0 put mqtt_manager.json
```

# MQTT Manager :: main loop example
```
from time import sleep
from gc import collect

# Connection to MQTT Broker
from mqtt_manager import MQTT_Manager
mqtt_client = MQTT_Manager()
print( 'client_id:', mqtt_client.CONFIG['client_id'] )
Done = False
print('MQTT check', end='')
while not Done:
  Done = mqtt_client.check()
  print('.', end='')
  sleep(1)
del(Done)
print()
collect()

# optional: Config comunication MQTT Topics 
TOPIC_SUB = mqtt_client.get_topic('control')
TOPIC_PUB = mqtt_client.get_topic('status')
chatty_client = bool(mqtt_client.CONFIG.get('chatty', True))


# optional: Subscribe to MQTT Topics status & control 
mqtt_client.broker.set_callback(MQTT_subscribe_callback_function)
mqtt_client.broker.subscribe(TOPIC_SUB)

mqtt_client.send(TOPIC_PUB, 'Hello World')
```


# Sensor Manager :: Setup
Send sensor_manager.py to board using:
```
ampy -p /dev/ttyUSB0 put sensors_manager.py
```

# Sensors Manager :: Using DHT22 (or DHT11) example
```
import machine, time

from sensor_manager import Sensor_DHT22 # or DHT11
sensor = Sensor_DHT22( 5 ) # Pin 5 = D1 

while True:
  sensor.read()
  print(sensor.values, sensor.values_dict)
  time.sleep(1)
```

# Sensor Manager :: Using DS18B20 example
```
import machine, time

from sensor_manager import Sensor_DS18B20
sensor = Sensor_DS18B20( 5 ) # Pin 5 = D1

while True:
  sensor.read()
  print(sensor.values, sensor.values_dict)
  time.sleep(1)
```

# Sensor Manager :: example using the BME280 (pressure, temperature and humidity sensor)
```
import machine, time

i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4)) # Pin 5 = D1 | Pin 4 = D2
from sensor_manager import Sensor_BME280
sensor = Sensor_BME280(i2c=i2c, address=0x76) # to find address use i2c.scan()

while True:
  sensor.read()
  print(sensor.values, sensor.values_dict)
  time.sleep(1)
```
Note: also need to put the file `bme280.py` in folder `libs` using: 
```
ampy -p /dev/ttyUSB0 put bme280.py bme280.py
```


# Sensor Manager :: example using the HC-SR04 (UltraSonic sensor) 
```
import machine, time

from sensor_manager import Sensor_HCSR04
sensor = Sensor_HCSR04(trigger=5, echo=4)

while True:
  sensor.read()
  print(sensor.values, sensor.values_dict, sensor.distance_mm, sensor.distance_cm)
  time.sleep(1)
```

# Sensor Manager :: example using the VL53L0X (Light Distance sensor) 
```
import machine, time

i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4)) # Pin 5 = D1 | Pin 4 = D2
from sensor_manager import Sensor_VL53L0X
sensor = Sensor_VL53L0X(i2c=i2c, address=0x29) # to find address use i2c.scan()

while True:
  sensor.read()
  print(sensor.values, sensor.values_dict)
  time.sleep(1)
```

# Sensor Manager :: example using the BH1750FVI (Lux sensor) 
```
import machine, time

i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4)) # Pin 5 = D1 | Pin 4 = D2
from sensor_manager import Sensor_BH1750FVI
sensor = Sensor_BH1750FVI(i2c=i2c, address=0x23) # to find address use i2c.scan()

while True:
  sensor.read()
  print(sensor.values, sensor.values_dict)
  time.sleep(1)
```
