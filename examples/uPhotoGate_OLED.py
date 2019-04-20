# filename: main_mqtt_oled.py
# WEMOS D1 Mini Board GPIO Map: D8 pull_down, D4 pull_down
# D0=16, D1=5, D2=4, D3=0, D4=2, D5=14, D6=12, D7=13, D8=15
import os, gc, micropython, machine, time, json

# Broker
# https://www.hivemq.com/public-mqtt-broker/
# TOPIC: devices/esp8266_f5ede900/status

GATE_PIN = micropython.const(13) # D7
GATE_MODE = micropython.const(0) # 0 for always on | 1 for always off
DEBUG = micropython.const(1) # Change from 1 debug mode to 0 production mode
DEBUG_TIME = micropython.const(10) # Run in debug mode for this amount of seconds
DELAY_TIME = micropython.const(1)  # Delay between loops
print('PhotoGate in MicroPython')

from wlan_manager import WLAN_Manager # Wireless Connection
wlan_client = WLAN_Manager()
wlan_client.start()

from mqtt_manager import MQTT_Manager # MQTT Connection
mqtt_client = MQTT_Manager()
mqtt_client.check() # Open connection to broker
TOPIC_SUB = mqtt_client.get_topic('control')
TOPIC_PUB = mqtt_client.get_topic('status')
print('Topic:', TOPIC_PUB)

# ssd1306 version
import ssd1306
i2c = machine.I2C(scl=machine.Pin(5), sda=machine.Pin(4))
oled = ssd1306.SSD1306_I2C(128, 64, i2c, 0x3c)

from sensor_manager import PhotoGate
g1 = PhotoGate(GATE_PIN, mode=GATE_MODE) # mode = 1 | 0

oled.fill(0)
oled.rect(0,0,128,40,1)
oled.text('PhotoGate', 28, 8)
oled.text('in MicroPython', 10, 24)
oled.text(mqtt_client.CONFIG['client_id'], 00, 48)
oled.text(mqtt_client.CONFIG['broker'], 00, 56)
oled.show()

def update_oled(data):
  oled.scroll(0, -8)
  oled.fill_rect(0, 56, 128, 64, 0)
  oled.text('{:10.3f}'.format(data), 0, 56)
  oled.show()

gc.collect()
while True:
  g1.read()
  if g1.event_change_to(1):
    g1.start_time()
  if g1.event_change_to(0):
    g1.stop_time()
    print(g1.millis)
    update_oled(g1.millis)
    msg = {'value': g1.millis, 'units': 'ms'}
    mqtt_client.send(TOPIC_PUB, json.dumps(msg))
    gc.collect()
  g1.store()
  if DEBUG:
    time.sleep_us(DEBUG_TIME)
  else:
    time.sleep_us(DELAY_TIME)
#End while loops


#if __name__ == '__main__':
#  main()
