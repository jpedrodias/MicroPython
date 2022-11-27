![MicroPython](software/micropythonpowered-art.png)
# MicroPython
> MicroPython is a full Python compiler and runtime that runs on the bare-metal. You get an interactive prompt (the REPL) to execute commands immediately, along with the ability to run and import scripts from the built-in filesystem. The REPL has history, tab completion, auto-indent and paste mode for a great user experience.


I built these tools to help me use MicroPython in my classroom 
(This was tested on Wemos D1 Mini - ESP8266)

# Contents
<ul>
  <li>how to use WLAN Manager</li>
  <li>how to use MQTT Manager</li>
  <li>how to use Sensors Manager</li>
  <li>how to use Board Manager (at work)</li>
  <li>how to use Robot Manager (at work) </li>
</ul>


*NOTE*: I created a custom version of MicroPython already with this files built in (wlan_manager, mqtt_manager, sensor_manager, board_manager and robot_manager). 
(You will find that custom version in the folder "<a href="conpiled">compiled</a>" )

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


# Board Manager
The board_manager has some useful tools and the GPIO map.

Send board_manager.py to board using:
```bash
ampy -p /dev/ttyUSB0 put board_manager.py
```  
Sample code to get GPIO:
```python
from machine import Pin
from board_manager import D4 # D0 to D8
    
led = Pin(D4, Pin.OUT)
for i in range(10):
    led.value(i % 2)

```

Sample code to use StatusLD:
```python 
from board_manager import D4, StatusLED
led = StatusLED(D4)
led.on()
    
for i in range(10):
    led.toggle()
```

Sample code to use NTP:
```python 
import ntptime # ntptime.settime()
ntptime.host = 'ntp02.oal.ul.pt'
    
from board_manager import NTPClock as Clock
clock = Clock()
print(clock)
```

    
# WLAN Manager :: Setup
Send wlan_manager.py to board using:
```bash
ampy -p /dev/ttyUSB0 put wlan_manager.py
```

The first time you need to run the `setup()` function. This function will creat the file wlan_manager.json to store SSID and password
Sample code:
```python
from wlan_manager import WLAN_Manager
wlan_client = WLAN_Manager()

wlan_client.setup() # creates wlan_manager.json file to store your SSID and password
wlan_client.setup('HOME', 'password', append=False) # overwrite the file and store this settings
wlan_client.setup('WORK', 'password', append=True)  # appends this settings to the file

wlan_client.start() # Start using data stored in wlan_manager.json file
wlan_client.start('HOME', 'password') # Start using this ssid and password
```


# MQTT Manager :: Setup
Send mqtt_manager.py and <b>mqtt_manager.json</b> (change here your mqtt setting before send) to board using:
```bash
ampy -p /dev/ttyUSB0 put mqtt_manager.py
ampy -p /dev/ttyUSB0 put mqtt_manager.json
```

Install dependencies on mcu:
```python
import mip
mip.install('umqtt.robust')
mip.install('umqtt.simple')
mip.install('ssd1306')
```

Sample code:
```python
from mqtt_manager import MQTT_Manager
mqtt_client = MQTT_Manager()
mqtt_client.setup() # creates mqtt_manager.json file to store your broker settings

mqtt_client.check()
mqtt_client.send("debug", "Hello World")
print( "client_id:", mqtt_client.CONFIG["client_id"] )
````

# WLAN and MQTT Manager :: main loop example
Sample code:
```python
def reconnect():
  wlan_client.start()
  success = wlan_client.check() and mqtt_client.check()
  if success:
    mqtt_client.broker.subscribe(TOPIC_SUB)
  return success

def mqtt_callback(topic, msg):
  print('MSG! Topic: {}; Data {}'.format(topic, msg))

from wlan_manager import WLAN_Manager
wlan_client = WLAN_Manager()

from mqtt_manager import MQTT_Manager
mqtt_client = MQTT_Manager()

TOPIC_SUB = mqtt_client.get_topic("control") # You talking to the sensor
TOPIC_PUB = mqtt_client.get_topic("status")  # The sensor talking to you
chatty_client =  bool(mqtt_client.CONFIG.get("chatty", True))
mqtt_client.broker.set_callback(mqtt_callback)
print( "client_id:", mqtt_client.CONFIG["client_id"] )

connected = reconnect()
if connected:
  mqtt_client.send("debug", TOPIC_SUB)
  mqtt_client.send("debug", TOPIC_PUB)
```


# Sensor Manager :: Setup
Send sensor_manager.py to board using:
```bash
ampy -p /dev/ttyUSB0 put sensors_manager.py
```


# Sensors Manager :: Using DHT22 (or DHT11) (temperature and humidity sensor)
Sample code:
```python
from machine import Pin
from time import sleep
from board_manager import D1 # D1, ... , D8
from sensor_manager import Sensor_DHT22 # or DHT11

sensor = Sensor_DHT22(D1)

while True:
  sensor.read()
  print(sensor.values, sensor.values_dict)
  sleep(1)
```


# Sensor Manager :: Using DS18B20 (temperature sensor)
Sample code:
```python
from machine import Pin
from time import sleep
from board_manager import D1 # D1, ... , D8
from sensor_manager import Sensor_DS18B20

sensor = Sensor_DS18B20(D1)

while True:
  sensor.read()
  print(sensor.values, sensor.values_dict)
  sleep(1)
```


# Sensor Manager :: Using BMP085, BMP180 or BME280 (pressure, temperature and humidity sensor)
Sample code:
```python
from machine import Pin, I2C
from time import sleep
from board_manager import D1, D2 # D1, ... , D8
from sensor_manager import Sensor_BME280 # Sensor_BME280 or Sensor_BMP180

i2c = I2C(scl=Pin(D1), sda=Pin(D2))
sensor = Sensor_BME280(i2c=i2c, address=0x76) # to find address use i2c.scan()

while True:
  sensor.read()
  print(sensor.values, sensor.values_dict)
  sleep(1)
```
Note: also need to put the file `bme280.py` (or `bme280.mpy`) in the root folder using: 
```bash
ampy -p /dev/ttyUSB0 put bme280.py bme280.py
```


# Sensor Manager :: Using HC-SR04 (UltraSonic distance sensor) 
Sample code:
```python
from machine import Pin
from time import sleep
from board_manager import D1, D2 # D1, ... , D8
from sensor_manager import Sensor_HCSR04

sensor = Sensor_HCSR04(trigger=D1, echo=D2) # or sensor = Sensor_HCSR04(D1, D2)

while True:
  sensor.read()
  print(sensor.values, sensor.values_dict, sensor.distance_mm, sensor.distance_cm)
  sleep(1)
```


# Sensor Manager :: Using VL53L0X (Light distance sensor) 
Sample code:
```python
from machine import Pin, I2C
from time import sleep
from board_manager import D1, D2 # D1, ... , D8
from sensor_manager import Sensor_VL53L0X

i2c = I2C(scl=Pin(D1), sda=Pin(D2))
sensor = Sensor_VL53L0X(i2c=i2c, address=0x29) # to find address use i2c.scan()

while True:
  sensor.read()
  print(sensor.values, sensor.values_dict)
  sleep(1)
```


# Sensor Manager :: Using BH1750FVI (Lux sensor) 
Sample code:
```python
from machine import Pin, I2C
from time import sleep
from board_manager import D1, D2 # D1, ... , D8
from sensor_manager import Sensor_BH1750FVI

i2c = I2C(scl=Pin(D1), sda=Pin(D2))
sensor = Sensor_BH1750FVI(i2c=i2c, address=0x23) # to find address use i2c.scan()

while True:
  sensor.read()
  print(sensor.values, sensor.values_dict)
  sleep(1)
```


# Sensor Manager :: Using PhotoGate
Sample code:
```python
from micropython import const
from sensor_manager import PhotoGate
from board_manager import D7 as GATE_PIN

GATE_MODE = const(0) # 0 for always on | 1 for always off
DELAY_TIME = const(1)

gate1 = PhotoGate(GATE_PIN, mode=GATE_MODE) # mode = 1 | 0
while True:
  gate1.read()
  if gate1.event_change_to(1):
    gate1.start_time()
  if gate1.event_change_to(0):
    gate1.stop_time()
    print(gate1.millis)
  gate1.store()
  time.sleep_us(DELAY_TIME)
#End while loop
```
<a href="./examples/06 PhotoGate MicroPython.pdf">show example</a>


# License

Any code placed here is released under the MIT License (MIT).  
The MIT License (MIT)  
Copyright (c) 2016 Peter Hinch  
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

# End of File
