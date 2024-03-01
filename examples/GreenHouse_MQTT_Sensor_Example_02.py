from machine import Pin, I2C
from json import loads, dumps
from time import sleep, sleep_ms, ticks_ms, ticks_diff

from gc import enable as gc_enable, collect as gc_collect
gc_enable()


from sensor_manager import Sensor_BME280
pin_scl = 9
pin_sda = 8
i2c = I2C(id=0, scl=Pin(pin_scl), sda=Pin(pin_sda))
sleep(1)
print(i2c.scan())
sensor1 = Sensor_BME280(i2c=i2c, address=0x76)


from wlan_manager import WLAN_Manager
wlan_client = WLAN_Manager()
wlan_client.start()

# Helper to reconnect 
def reconnect():
  wlan_client.start()
  success = wlan_client.check() and mqtt_client.check()
  if success:
    mqtt_client.broker.subscribe(TOPIC_SUB)
  return success


from mqtt_manager import MQTT_Manager
mqtt_client = MQTT_Manager()

def mqtt_callback(topic, msg):
    print('MSG! Topic: {}; Data {}'.format(topic, msg))


# Global variables
TOPIC_SUB = mqtt_client.get_topic("control") # You talking to the sensor
TOPIC_PUB = mqtt_client.get_topic("status")  # The sensor talking to you
CHAT_DELAY = mqtt_client.CONFIG.get("delay", 60)
chatty_client = bool(mqtt_client.CONFIG.get("chatty", True))
mqtt_client.broker.set_callback(mqtt_callback)
mqtt_client.check()

print( "client_id:", mqtt_client.CONFIG["client_id"] )
print( "MQTT SUB:", TOPIC_SUB)
print( "MQTT PUB:", TOPIC_PUB)


# Main Loop
gc_collect()
print('Ready')
i = 0
while True:
    ti = ticks_ms()
    connected = mqtt_client.check_msg()
    if not connected:
        connected = reconnect()
        sleep(1)
        continue
    
    sensor1.read()
    t, h, p = sensor1.values
    d = {"bme280": {"t": t, "h": h, "p": p}}
    status = mqtt_client.send(TOPIC_PUB, dumps(d))
    print(status, d)
    
    tf = ticks_ms()
    delta_t = ticks_diff(tf, ti)
    sleep_ms(CHAT_DELAY * 1000 - delta_t)

