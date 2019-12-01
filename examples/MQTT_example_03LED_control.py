from time import sleep
from machine import Pin
from board_manager import *
from json import dumps, loads
from wlan_manager import WLAN_Manager
from mqtt_manager import MQTT_Manager

wlan_client = WLAN_Manager()
mqtt_client = MQTT_Manager()

def reconnect():
  wlan_client.start()
  success = wlan_client.check() and mqtt_client.check()
  if success:
    mqtt_client.broker.subscribe(TOPIC_SUB)
  return success

def mqtt_callback(topic, msg):
  global status
  print('MSG! Topic: {};\nData: {}'.format(topic.decode(), msg.decode()))
  
  # Get the number 0 to 8 after /control/#
  try:
    object = int(topic.decode().split("/")[-1])
  except:
    print("Error getting the object.")
    return False
  
  try:
    value = int(msg.decode())
  except:
    print("Error getting the value.")
    return False
  
  status[ object ] = value
  return True

PREFIX = "Personal" # Put something personal
TOPIC_SUB = "/".join( [PREFIX, mqtt_client.get_topic("control"), "#"] )
TOPIC_PUB = "/".join( [PREFIX, mqtt_client.get_topic("status") ] )

chatty_client =  bool(mqtt_client.CONFIG.get("chatty", True))
mqtt_client.broker.set_callback(mqtt_callback)
print( "client_id:", mqtt_client.CONFIG["client_id"] )

connected = reconnect()
if connected:
  mqtt_client.send("debug", TOPIC_SUB)
  mqtt_client.send("debug", TOPIC_PUB)

G = Pin(D0, Pin.OUT, value = 0)
R = Pin(D1, Pin.OUT, value = 0)


objects = [G, R]
status = [object.value() for object in objects]
last_status = None

while True:
  sucess = mqtt_client.check_msg()
  if not sucess:
    sucess = mqtt_client.check()
    if not sucess: 
      sucess = reconnect()  
  
  if status != last_status:
    print("Data changed")
    for index, object in enumerate(objects):
      object.value( status[index] )
      topic = "{}/{}".format( TOPIC_PUB, index )
      data = dumps( status[index] ) 
      mqtt_client.send( topic, data )
      
    last_status = [s for s in status]
    
  sleep(1)
