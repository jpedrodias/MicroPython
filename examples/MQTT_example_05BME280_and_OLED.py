from machine import Pin, I2C
from utime import sleep_ms, ticks_ms, ticks_diff
from ujson import dumps

from wlan_manager import WLAN_Manager
from mqtt_manager import MQTT_Manager

from board_manager import  D1, D2
from sensor_manager import Sensor_BME280
from ssd1306 import SSD1306_I2C

i2c = I2C(scl=Pin(D1), sda=Pin(D2))

sensor = Sensor_BME280(i2c=i2c, address=118) # i2c.scan()
oled = SSD1306_I2C(128, 64, i2c, 0x3c)

wlan_client = WLAN_Manager()
mqtt_client = MQTT_Manager()

#wlan_client.setup('ATLANTICO', 'oceano12', append=False)
#wlan_client.start()

def reconnect():
  wlan_client.start()
  success = wlan_client.check() and mqtt_client.check()
  if success:
    mqtt_client.broker.subscribe(TOPIC_SUB)
  return success

def mqtt_callback(topic, msg):
  print('MSG! Topic: {}; Data {}'.format( topic, msg ))

TOPIC_SUB = mqtt_client.get_topic("control")
TOPIC_PUB = mqtt_client.get_topic("status")

chatty_client =  bool(mqtt_client.CONFIG.get("chatty", True))
mqtt_client.broker.set_callback(mqtt_callback)
print( "client_id:", mqtt_client.CONFIG["client_id"] )


pub_str = ["ColegioAtlantico", "*Clube Robotica*"]
pub_idx = 0
pub_counts = 10
pub_i = 0


DELAY = 1000 
while True:
  t_start = ticks_ms()
  
  sensor.read()
  if not mqtt_client.check():
    reconnect()
  
  print( sensor.values_dict )
  mqtt_client.send(TOPIC_PUB, dumps( sensor.values_dict ))
  
  oled.fill(0)
  oled.text("*Clube Robotica*" , 2, 4)
  oled.rect(0,14,128,38,1)
  oled.text("T: {} C".format( sensor.t ) , 8, 20)
  oled.text("H: {} %".format( sensor.h ) , 8, 30)
  oled.text("P: {} hPa".format( sensor.p ) , 8, 40)
  
  if pub_i == 0:
    pub_idx = (pub_idx + 1 ) % len(pub_str)
  pub_i = (pub_i + 1 ) % pub_counts
  
  oled.text( pub_str[pub_idx] , 0, 56)
  oled.show()
  
  # PAUSA ENTRE LOOPS
  while ticks_diff(ticks_ms(), t_start) <= DELAY:
    mqtt_client.check_msg() # check for new messages
    sleep_ms(100)

#End while True
