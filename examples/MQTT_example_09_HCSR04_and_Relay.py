#filename MQTT Ultrasonic Relay
from machine import Pin
from time import sleep

from wlan_manager import WLAN_Manager
from mqtt_manager import MQTT_Manager
from json import dumps, loads

from board_manager import D1, D5, D6, D7
from sensor_manager import Sensor_HCSR04

def reconnect():
  led.value( 1 )
  print("WiFi Connection")
  if not wlan_client.check():
    wlan_client.start()
    sleep(5)
  for i in range(30):
    if wlan_client.check(): break
    print(".", end="")
    sleep(1)
    led.value( not led.value() )
  success = wlan_client.check() and mqtt_client.check()
  if success:
    mqtt_client.broker.subscribe(TOPIC_SUB)
  return success
  
def mqtt_callback(topic, msg):
  global status
  led.value( 1 )
  print('Mensagem! Topic: {};\nData: {}'.format(topic.decode(), msg.decode()))
  # Get the number 0 to 8 after /control/#
  try:
    object = int(topic.decode().split("/")[-1])
  except:
    print("Erro ao tentar ter objeto.")
    return False
  try:
    value = int(msg.decode())
  except:
    print("Erro ao tentar ter valor.")
    return False
  if object not in [i for i in range(len(objects))] or value not in [0, 1]:
    print("Error in Object={} or value={}".format(object, value))
    return False
  status[ object ] = value
  return True

wlan_client = WLAN_Manager()
mqtt_client = MQTT_Manager()

sensor = Sensor_HCSR04(D5, D6)
relay = Pin(D1, Pin.OUT, value = 0)
led = Pin(D7, Pin.OUT, value = 0)

PREFIX = "Personal"
TOPIC_SUB = "/".join( [PREFIX, mqtt_client.get_topic("control"), "#"] )
TOPIC_PUB = "/".join( [PREFIX, mqtt_client.get_topic("status") ] )
chatty_client =  bool(mqtt_client.CONFIG.get("chatty", True))
mqtt_client.broker.set_callback(mqtt_callback)

print( "client_id:", mqtt_client.CONFIG["client_id"] )

connected = reconnect()
if connected:
  mqtt_client.send("debug", TOPIC_SUB)
  mqtt_client.send("debug", TOPIC_PUB)
  
objects = [relay]
status = [1 for object in objects]
last_status = [0 for object in objects]

LIMITE = 100
LIMITE_off = 60
count2off = 0

while True:
  sucess = mqtt_client.check_msg()
  if not sucess:
    sucess = mqtt_client.check()
    if not sucess:
      sucess = reconnect() 
  sensor.read()
  d = sensor.distance_cm
  print(d, d < LIMITE)

  if 2 < d < LIMITE:
    status[0] = 1
  for i in range(len(objects)):
    if status[i] != last_status[i]:
      print("Data Changed")
      objects[i].value( status[i] )
      topic = "{}/{}".format( TOPIC_PUB, i )
      data = dumps( status[i] )
      mqtt_client.send( topic, data )
      last_status[i] = status[i]
      if status[0]:
        count2off = LIMITE_off
  if status[0]:
    if count2off:
      count2off -= 1
    else:
      status[0] = 0
  print("Status", status[0], "count2off", count2off) 
  led.value( not led.value() )
  sleep(1)
#End of while
#End of file
