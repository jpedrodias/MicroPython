# MicroPython
Some tools to help when using MicroPython (tested on Wemos D1 Mini - esp8266)

<ul>
  <li>how to use WLAN Manager</li>
  <li>how to use MQTT Manager</li>
  <li>how to use Sensors Manager</li>
  <li>how to use Board Manager (at work)</li>
  <li>how to use Robot Manager (at work) </li>
</ul>


PS: My personilized version of MicroPython in compiled folder, already has this files (wlan_manager, mqtt_manager, sensor_manager, board_manager and robot_manager) 


# Wemos D1 mini :: GPIO MAP
<table>
<tr><TD>PIN: <TD>D0<TD>D1<TD>D2<TD>D3<TD>D4<TD>D5<TD>D6<TD>D7<TD>D8
<TR><TD>GPIO:<TD>16<TD> 5<TD> 4<TD> 0<TD> 2<TD>14<TD>12<TD>13<TD>15
<TR><TD>PWM: <TD> N<TD> Y<TD> Y<TD> Y<TD> Y<TD> Y<TD> Y<TD> Y<TD> Y
</table>


# Wemos D1 mini :: Boot Mode Options
<table>
  <tr><td>GPIO15<td>GPIO0<td>GPIO2<td>Mode <td>Comment
  <tr><td> D8 <td> D3 <td> D4 <td>  <td>Comment
  <tr><td>L     <td>H    <td>H    <td>Flash<td>boot from SPI Flash  
  <tr><td>L     <td>L    <td>H    <td>UART<td>Program via UART (TX/RX)
  <tr><td>H     <td>any  <td>any  <td>SDIO<td>Boot from SD card
</table>


# WLAN Manager :: Setup
Send wlan_manager.py to board using:
```
ampy -p /dev/ttyUSB0 put wlan_manager.py
```

The first time you need to run the `setup()` function. This function will creat the file wlan_manager.json to store SSID and password
```
from wlan_manager import WLAN_Manager
wlan_client = WLAN_Manager()
wlan_client.setup() # creates wlan_manager.json file to store your SSID and password
wlan_client.setup('HOME', 'password', append=False) # overwrite the file and store this settings
wlan_client.setup('WORK', 'password', append=True)  # appends this settings to the file
wlan_client.start()
```


# MQTT Manager :: Setup
Send mqtt_manager.py and <b>mqtt_manager.json</b> (change here your mqtt setting before send) to board using:
```
ampy -p /dev/ttyUSB0 put mqtt_manager.py
ampy -p /dev/ttyUSB0 put mqtt_manager.json
```

from mqtt_manager import MQTT_Manager
mqtt_client = MQTT_Manager()
mqtt_client.setup() # creates mqtt_manager.json file to store your broker settings
print( 'client_id:', mqtt_client.CONFIG['client_id'] )


# WLAN and MQTT Manager :: main loop example
```
def reconnect():
  wlan_client.start()
  success = wlan_client.check() and mqtt_client.check()
  if success:
    mqtt_client.broker.subscribe(TOPIC_SUB)
  return success
  
from wlan_manager import WLAN_Manager
wlan_client = WLAN_Manager()

from mqtt_manager import MQTT_Manager
mqtt_client = MQTT_Manager()

TOPIC_SUB = mqtt_client.get_topic('control') # You talking to the sensor
TOPIC_PUB = mqtt_client.get_topic('status')  # The sensor talking to you
chatty_client =  bool(mqtt_client.CONFIG.get('chatty', True))
mqtt_client.broker.set_callback(mqtt_callback)
print( 'client_id:', mqtt_client.CONFIG['client_id'] )

connected = reconnect()
if connected:
  mqtt_client.send('debug', TOPIC_SUB)
  mqtt_client.send('debug', TOPIC_PUB)
  mqtt_client.send('debug', app_name)
```


# Sensor Manager :: Setup
Send sensor_manager.py to board using:
```
ampy -p /dev/ttyUSB0 put sensors_manager.py
```


# Sensors Manager :: Using DHT22 (or DHT11) example (temperature and humidity sensor)
```
import machine, time

from sensor_manager import Sensor_DHT22 # or DHT11
sensor = Sensor_DHT22( 5 ) # Pin 5 = D1 

while True:
  sensor.read()
  print(sensor.values, sensor.values_dict)
  time.sleep(1)
```


# Sensor Manager :: Using DS18B20 example (temperature sensor)
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
Note: also need to put the file `bme280.py` (or `bme280.mpy`) in the root folder using: 
```
ampy -p /dev/ttyUSB0 put bme280.py bme280.py
```


# Sensor Manager :: example using the HC-SR04 (UltraSonic distance sensor) 
```
import machine, time

from sensor_manager import Sensor_HCSR04
sensor = Sensor_HCSR04(trigger=5, echo=4)

while True:
  sensor.read()
  print(sensor.values, sensor.values_dict, sensor.distance_mm, sensor.distance_cm)
  time.sleep(1)
```


# Sensor Manager :: example using the VL53L0X (Light distance sensor) 
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

# End of File
