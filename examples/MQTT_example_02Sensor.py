import machine, time, json

from wlan_manager import WLAN_Manager # Wireless Connection 
from mqtt_manager import MQTT_Manager # MQTT Connection

wlan_client = WLAN_Manager()
mqtt_client = MQTT_Manager()

def reconnect():
  wlan_client.start()
  success = wlan_client.check() and mqtt_client.check()
  if success:
    mqtt_client.broker.subscribe(TOPIC_SUB)
  return success

def mqtt_callback(topic, msg):
  print('MSG! Topic:{}; Data{}'.format(topic, msg))
  
TOPIC_SUB = mqtt_client.get_topic('control')
TOPIC_PUB = mqtt_client.get_topic('status')

print("TOPIC_SUB", TOPIC_SUB)
print("TOPIC_PUB", TOPIC_PUB)

mqtt_client.broker.set_callback(mqtt_callback)
mqtt_client.broker.subscribe(TOPIC_SUB)

# Change this to your sensor
from board_manager import D1
from sensor_manager import Sensor_DS18B20
sensor = Sensor_DS18B20(D1) # Pin 5 = D1

DELAY = 5 * 1000 # DELAY in milliseconds
while True:
  sensor.read()
  msg = sensor.values_dict
  print(msg)
  mqtt_client.send(TOPIC_PUB, json.dumps(msg))
  t_start = time.ticks_ms()
  while time.ticks_diff(time.ticks_ms(), t_start) <= DELAY:
    mqtt_client.check_msg() # check for new messages
    time.sleep_ms(200)
#End main loop
