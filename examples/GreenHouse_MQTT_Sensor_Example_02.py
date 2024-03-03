import machine # Pin, I2C, RTC
import gc      # enable, collect, mem_free
import time    # sleep, sleep_me, ticks_ms, ticks_diff
import ntptime # host
import json    # loads, dumps

USE_SENSOR_BME280 = True
USE_SENSOR_SOIL_M = True
USE_SENSOR_DS18B20= False

# WLAN - Wireless Local Area Network
from wlan_manager import WLAN_Manager
wlan_client = WLAN_Manager()
wlan_client.start()

# MQTT - Message Queuing Telemetry Transport
from mqtt_manager import MQTT_Manager
mqtt_client = MQTT_Manager()

# NTP - Network Time Protocol
ntptime.host = 'pool.ntp.org'
ntptime_query_delay = 3600000 * 24 # 1h
ntptime_last_update = time.ticks_ms() - ntptime_query_delay

# I2C - Inter-Integrated Circuit Protocol
if USE_SENSOR_BME280:
    PIN_I2C_SCL, PIN_I2C_SDA = 9, 8
    i2c = machine.I2C(id=0, scl=machine.Pin(PIN_I2C_SCL), sda=machine.Pin(PIN_I2C_SDA))
    from sensor_manager import Sensor_BME280
    sensor_bme280 = Sensor_BME280(i2c=i2c, address=0x76)

# ADC - Analogue Digital Converter
if USE_SENSOR_SOIL_M:
    from sensor_manager import Sensor_ADC
    sensor_soil_h = Sensor_ADC(0)

# DS18B20 - One Wire Protocol
if USE_SENSOR_DS18B20:
    from sensor_manager import Sensor_DS18B20
    PIN_OneWire = 17
    sensor_ds18b20 = Sensor_DS18B20(PIN_OneWire)


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

sensors_data = {'localtime': "", 'mem_free': 0}
if USE_SENSOR_BME280: sensors_data['bme280'] = {}
if USE_SENSOR_SOIL_M: sensors_data['soil_moisture'] = {}
if USE_SENSOR_DS18B20: sensors_data['ds18b20'] = {}
    
while True:
    ti = time.ticks_ms()
    connected = mqtt_client.check_msg()
    if not connected:
      connected = reconnect()
      sleep(1)
      continue
    
    if USE_SENSOR_BME280:
      sensor_bme280.read()
      sensors_data['bme280'] = sensor_bme280.values_dict
    
    if USE_SENSOR_SOIL_M:
      sensor_soil_h.read()
      sensors_data['soil_moisture'] = sensor_soil_h.values_dict
    
    if USE_SENSOR_DS18B20:
      sensor_ds18b20.read()
      sensors_data['ds18b20'] = sensor_ds18b20.values_dict
      
    localtime = time.localtime()
    sensors_data['localtime'] = "{:0>4d}-{:0>2d}-{:0>2d} {:0>2d}:{:0>2d}:{:0>2d}".format(*localtime)
    sensors_data['mem_free'] = gc.mem_free()
    
    # Publish to MQTT Broker
    status = mqtt_client.send(TOPIC_PUB, json.dumps(sensors_data))
    print(sensors_data)
    if not status: print('Warning: data not send!')

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

