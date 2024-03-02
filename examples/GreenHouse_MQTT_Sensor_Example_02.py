import machine # Pin, I2C, RTC
import gc      # enable, collect, mem_free
import time    # sleep, sleep_me, ticks_ms, ticks_diff
import ntptime # host
import json    # loads, dumps


# WLAN - Wireless Local Area Network
from wlan_manager import WLAN_Manager
wlan_client = WLAN_Manager()
wlan_client.start()

# MQTT - Message Queuing Telemetry Transport
from mqtt_manager import MQTT_Manager
mqtt_client = MQTT_Manager()

# NTP - Network Time Protocol
ntptime.host = 'pool.ntp.org'
ntptime_query_delay = 3600000 # 1h
ntptime_last_update = time.ticks_ms() - ntptime_query_delay

# I2C - Inter-Integrated Circuit Protocol
PIN_SCL, PIN_SDA = 9, 8
i2c = machine.I2C(id=0, scl=machine.Pin(PIN_SCL), sda=machine.Pin(PIN_SDA))
from sensor_manager import Sensor_BME280
sensor_bme280 = Sensor_BME280(i2c=i2c, address=0x76)

# ADC - Analogue Digital Converter
from sensor_manager import Sensor_ADC
sensor_soil_h = Sensor_ADC(0)

# GC - Garbage Collector attempts to reclaim memory
gc.enable()

def ntptime_update():
  global time, ntptime, ntptime_query_delay, ntptime_last_update
  need_update = False
  if time.ticks_ms() - ntptime_last_update >= ntptime_query_delay:
    need_update = True
    error = False
    try:
      ntptime.settime()
    except:
      error = True
  return need_update, not error

# Helper to reconnect to Wifi and MQTT Broker
def reconnect():
  global wlan_client, mqtt_client, TOPIC_SUB
  wlan_client.start()
  success = wlan_client.check() and mqtt_client.check()
  if success:
    mqtt_client.broker.subscribe(TOPIC_SUB)
  return success

def mqtt_callback(topic, msg):
    print('MSG! Topic: {}; Data {}'.format(topic, msg))


# MQTT Global Variables
TOPIC_SUB = mqtt_client.get_topic('control') # You talking to the sensor
TOPIC_PUB = mqtt_client.get_topic('status')  # The sensor talking to you
mqtt_chat_delay = mqtt_client.CONFIG.get('delay', 60)
mqtt_chatty_client = bool(mqtt_client.CONFIG.get('chatty', True))
mqtt_client.broker.set_callback(mqtt_callback)
mqtt_client.check()

print( 'client_id:', mqtt_client.CONFIG['client_id'] )
print( 'MQTT SUB:', TOPIC_SUB)
print( 'MQTT PUB:', TOPIC_PUB)


# Main Loop
gc.collect()
print('Setup Done')
while True:
    ti = time.ticks_ms()
    connected = mqtt_client.check_msg()
    if not connected:
        connected = reconnect()
        sleep(1)
        continue
    
    sensors_data = {
      'localtime': "",
      'bme280': {},
      'soil_moisture': {},
      'ds18b20': {}
    }
    sensor_bme280.read()
    t, h, p = sensor_bme280.values
    sensors_data['bme280'] = {'t': t, 'h': h, 'p': p}
    
    sensor_soil_h.read()
    h, = sensor_soil_h.values
    sensors_data['soil_moisture'] = {'h': h}
    
    localtime = time.localtime()
    sensors_data['localtime'] = "{:0>4d}-{:0>2d}-{:0>2d} {:0>2d}:{:0>2d}:{:0>2d}".format(*localtime)
    
    # Publish to MQTT Broker
    status = mqtt_client.send(TOPIC_PUB, json.dumps(sensors_data))
    print(status, sensors_data)

    # Update Internal clock
    status = ntptime_update()
    
    # Drift to 00 seconds
    drift = 1000 if localtime[5] % mqtt_chat_delay != 0 else 0
    if drift:
      print("Drifting", drift)
      #print(round(time.ticks_ms() / 1000), localtime[5], localtime[5] % mqtt_chat_delay)
    
    tf = time.ticks_ms()
    delta_t = time.ticks_diff(tf, ti)
    time.sleep_ms(mqtt_chat_delay * 1000 - delta_t - drift)

