from machine import Pin, I2C
from utime import sleep_ms, ticks_ms, ticks_diff
from ujson import dumps
from ucollections import OrderedDict

from wlan_manager import WLAN_Manager
from mqtt_manager import MQTT_Manager

from sensor_manager import Sensor_BME280
from board_manager import  D1, D2

from ssd1306 import SSD1306_I2C

i2c = I2C(scl=Pin(D1), sda=Pin(D2))

sensor = Sensor_BME280(i2c=i2c, address=118) # i2c.scan()
oled = SSD1306_I2C(128, 64, i2c, 0x3c)
oled.text("Loading ...", 0, 0)
oled.show()

wlan_client = WLAN_Manager()
mqtt_client = MQTT_Manager()

def reconnect(attempts=0):
  wlan_client.start(attempts=attempts)
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


DELAY = mqtt_client.CONFIG["delay"] * 1000 
while True:
  t_start = ticks_ms()
  
  sensor.read()
  t = sensor.values_dict['t']
  h = sensor.values_dict['h']
  p = sensor.values_dict['p']
  
  data = OrderedDict( [ ('t', t), ('h', h), ('p', p) ] )
  print( dumps(data) )
  
  is_online = mqtt_client.check()
  if not is_online:
    is_online = reconnect()
  
  if is_online:
    mqtt_client.send( TOPIC_PUB, dumps(data) )
  
  oled.fill(0)
  oled.text("*Clube Robotica*" , 1, 4)
  oled.rect(0,14,128,38,1)
  oled.text("T: {} C".format( t ) , 10, 20)
  oled.text("H: {} %".format( h ) , 10, 30)
  oled.text("P: {} hPa".format( p ) , 10, 40)
  oled.show()
  
  if gc.mem_free() < 10000:
    gc.collect()
    
  # PAUSE
  while ticks_diff(ticks_ms(), t_start) <= DELAY:
    if is_online: mqtt_client.check_msg()
    sleep_ms(100)

#End while True
