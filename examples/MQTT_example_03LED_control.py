from time import sleep, sleep_ms
from machine import Pin
from board_manager import *
from wlan_manager import WLAN_Manager
from mqtt_manager import MQTT_Manager
from sensor_manager import Sensor_HCSR04
from ssd1306 import SSD1306_I2C
from json import dumps, loads

#Ligação i2C
i2c = machine.I2C(scl=Pin(D1), sda=Pin(D2))
#Ligação ao Display OLED
oled = SSD1306_I2C(128, 64, i2c, 0x3c)

# Ligação ao sensor ultrasónico
sensor = Sensor_HCSR04(D3, D4)


wlan_client = WLAN_Manager()
mqtt_client = MQTT_Manager()

def reconnect():
  print("Coneccao WiFi")
  wlan_client.start()
  for i in range(30):
    if wlan_client.check(): break
    print(".", end="")
    sleep(1)
  sleep(5)
  success = wlan_client.check() and mqtt_client.check()
  if success:
    mqtt_client.broker.subscribe(TOPIC_SUB)
  return success
  
def mqtt_callback(topic, msg):
  global status
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
  
PREFIX = "Atlantico"
TOPIC_SUB = "/".join( [PREFIX, mqtt_client.get_topic("control"), "#"] ) #Canal onde recebe e interpreta as mensagens
TOPIC_PUB = "/".join( [PREFIX, mqtt_client.get_topic("status") ] ) #Canal onde manda as mensagens
chatty_client =  bool(mqtt_client.CONFIG.get("chatty", True))
mqtt_client.broker.set_callback(mqtt_callback)

print( "client_id:", mqtt_client.CONFIG["client_id"] ) #Para saber o client_id

connected = reconnect()
if connected:
  mqtt_client.send("debug message", TOPIC_SUB)
  mqtt_client.send("debug message", TOPIC_PUB)


# Ligação aos LEDs
G = Pin(D7, Pin.OUT, value=0)
Y = Pin(D6, Pin.OUT, value=0)
R = Pin(D5, Pin.OUT, value=0)

objects = [G, Y, R]
status = [object.value() for object in objects]
last_status = [0 for i in range(len(objects))]

while True:
  sucess = mqtt_client.check_msg()
  if not sucess:
    sucess = mqtt_client.check()
    if not sucess: 
      sucess = reconnect()  
  
  for i in range(len(objects)):
    if status[i] != last_status[i]:
      print("Data Changed")
      objects[i].value( status[i] )
      topic = "{}/{}".format( TOPIC_PUB, i )
      data = dumps( status[i] )
      mqtt_client.send( topic, data ) # reports back status
      last_status[i] = status[i]
  sleep(1)
