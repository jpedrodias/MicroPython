# Sensor_MAIN_APP | main.py | v0.5
import micropython
import machine
import json
import gc
import time    # time.sleep()
import ntptime # ntptime.settime()

DEBUG = False  # Exit Infinit Loop if DEBUG is True
ntptime.host = 'ntp02.oal.ul.pt'
app_name = 'APP: MicroPython + MQTT'
print( app_name )

def mqtt_callback(topic, msg):
  global chatty_client, main_delay
  if DEBUG: print(topic, msg)
  if msg == b'S':
    check_status(True)
  if msg == b'chatty on':
    chatty_client = True
  if msg == b'chatty off':
     chatty_client = False
  if msg.startswith(b'delay'):
    try:
      main_delay = int(msg.split()[1])
    except:
      pass
  if msg == b'R':
    machine.reset()

def check_status(publish=False):
  data = {
  'chatty': chatty_client,'delay': main_delay,
  'clientId': client_id,'timestamp': clock.timestamp,
  'datetime': clock.time}
  try:
    sensor.read() # read from sensor
  except:
    return False
  
  for key, value in sensor.values_dict.items():
    data[key] = value
    print(key, '=', value, ';', end=' ')
  print()
  if publish:
    try:
      mqtt_client.send(TOPIC_PUB, json.dumps(data))
    except:
      print('MQTT send failed!')
  return True

def reconnect():
  global wlan_client, mqtt_client
  wlan_client.start()
  print("MQTT check...")
  success = wlan_client.check()
  if success:
    clock.update()
  success = success and mqtt_client.check()
  if success:
    mqtt_client.broker.subscribe(TOPIC_SUB)
  return success

# Garbage Collector
gc.enable()
gc.collect()

# Connection to NTP 
from board_manager import NTPClock as Clock
clock = Clock()

# Hardware connection to status LED on D6
from board_manager import StatusLED, D6
led = StatusLED(D6)
led.on()

# Hardware connection to i2c and BME280 sensor
from board_manager import D1, D2
from sensor_manager import Sensor_BME280
i2c = machine.I2C(scl=machine.Pin(D1), sda=machine.Pin(D2)) # Pin 5 = D1 | Pin 4 = D2
sensor = Sensor_BME280(i2c=i2c, address=0x77)
sensor.read()

# Wireless connection 
from wlan_manager import WLAN_Manager
wlan_client = WLAN_Manager()
wlan_client.stop()

# Connection to MQTT broker 
from mqtt_manager import MQTT_Manager
mqtt_client = MQTT_Manager()
mqtt_client.broker.keepalive = 3600 # required for mosquitto v2

# GET MQTT SETTINGS from json file
TOPIC_SUB = mqtt_client.get_topic('control')
TOPIC_PUB = mqtt_client.get_topic('status')

chatty_client =  bool(mqtt_client.CONFIG.get('chatty', True))
client_id = mqtt_client.CONFIG['client_id']
mqtt_client.broker.set_callback(mqtt_callback)

print( 'client_id:', mqtt_client.CONFIG['client_id'] )

# First Wireless connection
connected = reconnect()
if DEBUG and connected:
  mqtt_client.send('debug', TOPIC_SUB)
  mqtt_client.send('debug', TOPIC_PUB)
  mqtt_client.send('debug', app_name)
gc.collect()

time.sleep(1)

if __name__ == '__main__':
  main_delay = mqtt_client.CONFIG['delay']
  if DEBUG: main_delay = 5
  Loops = 60
  gc.collect()
  try:
    while Loops:
      t_start = time.ticks_ms()
      if DEBUG: Loops -= 1
      led.on()
      if chatty_client:
        check_status(chatty_client and connected)
      while time.ticks_diff(time.ticks_ms(), t_start) <= main_delay * 1000:
        connected = mqtt_client.check_msg()
        if not connected:
          connected = reconnect()
          if not connected:
            connected = reconnect()
            time.sleep(4.5)
        led.toggle()
        time.sleep(0.5)
      #end while sleep loop
      gc.collect()
      if DEBUG: print('free mem:', gc.mem_free())
    #end while main loop
  except:
    pass
  mqtt_client.close()
  print(app_name)
  led.off()
  print('Rebooting')
  time.sleep(main_delay)
  machine.reset()
#end if __main__
