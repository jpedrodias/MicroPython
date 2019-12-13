# Modulos do MicroPython
from machine import Pin, I2C

from time import sleep
from json import dumps, loads

# Modulos de Ligação á Internet
from wlan_manager import WLAN_Manager
from mqtt_manager import MQTT_Manager

# Modulos de Ligação ao Hardware
from board_manager import *
from sensor_manager import Sensor_BME280
from sensor_manager import Sensor_BH1750

# Ligação à Internet
wlan_client = WLAN_Manager() # Cliente para ligar ao Wireless
#wlan_client.setup("ATLANTICO", "oceno12")
mqtt_client = MQTT_Manager() # Cliente para ligar ao Servidor de Mensagens

# Ligação ao Hardware
i2c = I2C(scl=Pin(D1), sda=Pin(D2)) # Protocolo de Comunicação I2C
sensor1 = Sensor_BME280(i2c, 118)   # Ligação ao sensor 1
sensor2 = Sensor_BH1750(i2c, 35)    # Ligação ao sensor 2

# Função para tratar das quedas de ligação à Internet
def reconnect():
  print("WiFi Connection")
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

# Função para tratar as mensagens recebidas
def mqtt_callback(topic, msg):
  print('MSG! Topic:{}; Data{}'.format(topic, msg))
  
# Topicos para enviar e receber mensagens
PREFIX = "Atlantico"
TOPIC_SUB = "/".join( [PREFIX, mqtt_client.get_topic("control"), "#"] )
TOPIC_PUB = "/".join( [PREFIX, mqtt_client.get_topic("status") ] )
mqtt_client.broker.set_callback(mqtt_callback)

DELAY = 5 * 1000 # DELAY in milliseconds

sucess = reconnect()
while True:
  sucess = mqtt_client.check_msg()
  if not sucess:
    sucess = mqtt_client.check()
    if not sucess: 
      sucess = reconnect()  
  
  sensor1.read()
  sensor2.read()
  t = sensor1.values_dict["t"]
  p = sensor1.values_dict["p"]
  l = sensor2.values_dict["lux"]
  
  values = {"t": t, "p": p, "l": l}
  data = dumps( values )
  print(msg)
  mqtt_client.send(TOPIC_PUB, data)
  sleep( DELAY )
