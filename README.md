# MicroPython
Some tools to help when using MicroPython

<ul>
  <li>how to use wlan manager</li>
  <li>how to use mqtt manager</li>
  <li>how to use sensors manager</li>
</ul>



# wlan manager :: setup
Send wlan_manager.py to board using:
```
ampy -p /dev/ttyUSB0 put wlan_manager.py
```

The first time you need to run the `setup()` function. This function will creat the file wlan_manager.json to store SSID and password
```
from wlan_manager import *
wlan_client = WLAN_Manager()
wlan_client.setup()
wlan_client.start()
```

# wlan manager :: main loop example
```
# Connection to Wireless
from gc import collect
from wlan_manager import *
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

# mqtt manager :: setup
Send mqtt_manager.py and mqtt_manager.json (change where your mqtt setting first) to board using:
```
ampy -p /dev/ttyUSB0 put mqtt_manager.py
ampy -p /dev/ttyUSB0 put mqtt_manager.json
```

# mqtt manager :: main loop example
```
# Connection to MQTT Broker
from gc import collect
from mqtt_manager import *
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
chatty_client =  bool(mqtt_client.CONFIG.get('chatty', True))


# optional: Subscribe to MQTT Topics status & control 
mqtt_client.broker.set_callback(MQTT_subscribe_callback_function)
mqtt_client.broker.subscribe(TOPIC_SUB)
```


# sensors manager :: setup
Send sensors_manager.py to board using:
```
ampy -p /dev/ttyUSB0 put sensors_manager.py
```

# Sensors manager :: BME280 example
```
from gc import collect
from machine import Pin, I2C

i2c = I2C(scl=Pin(5), sda=Pin(4)) # Pin 5 = D1 | Pin 4 = D2
from sensors_manager.py import Sensor_BME280
sensor = Sensor_BME280(i2c=i2c, address=0x76) # to find address use i2c.scan()
sensor.read()
sensor.values
sensor.values_dict
```
