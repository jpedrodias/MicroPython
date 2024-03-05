import machine # Pin, I2C, RTC
import gc      # enable, collect, mem_free
import time    # sleep, sleep_me, ticks_ms, ticks_diff
import ntptime # host
import json    # loads, dumps

USE_SENSOR_BME280 = True
USE_SENSOR_SOIL_M = True
USE_SENSOR_DS18B20= True
USE_SENSOR_STATUS_LED = True

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

if USE_SENSOR_STATUS_LED:
  from sensor_manager import StatusLED
  status_led = StatusLED(16)
  status_led.on()

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
   
def sensores_publish():
  global gc, time
  global USE_SENSOR_BME280, USE_SENSOR_SOIL_M, USE_SENSOR_DS18B20, USE_SENSOR_STATUS_LED
  global mqtt_client, sensor_bme280, sensor_soil_h, sensor_ds18b20
  global localtime, sensors_data, status_led
  
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
  if not status:
    print('Warning: data not send!')
  
  return status


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

sensors_data = {'localtime': "", 'mem_free': gc.mem_free()}
if USE_SENSOR_BME280:  sensors_data['bme280'] = {}
if USE_SENSOR_SOIL_M:  sensors_data['soil_moisture'] = {}
if USE_SENSOR_DS18B20: sensors_data['ds18b20'] = {}
localtime = time.localtime()

while True:
  t_start = time.ticks_ms()
  if USE_SENSOR_STATUS_LED: status_led.on()
  connected = mqtt_client.check_msg()
  if not connected:
    time.sleep(1)
    if USE_SENSOR_STATUS_LED: status_led.toggle()
    connected = reconnect()
    continue
  
  status = sensores_publish() # Main Job
  status = ntptime_update()   # Optional
  gc.collect()
  if USE_SENSOR_STATUS_LED: status_led.off()
  
  
  t_end = time.ticks_ms()
  drift = 1000 + t_end % 1000 if localtime[5] % mqtt_chat_delay != 0 else 0 # Drift to 00 seconds
  t_wait_start = time.ticks_ms()
  while time.ticks_diff(time.ticks_ms(), t_start) <= mqtt_chat_delay * 1000 - drift: # Fancy Waiting Loop
    #time.sleep_ms(mqtt_chat_delay * 1000 - delta_t - drift)
    connected = mqtt_client.check_msg()
    if not connected:
      if USE_SENSOR_STATUS_LED: status_led.toggle()
      time.sleep(1)
      connected = reconnect()
      continue
    time.sleep_ms(1)

    delta_t = time.ticks_diff(time.ticks_ms(), t_wait_start)
    if delta_t > 500:
      t_wait_start = time.ticks_ms()
      if USE_SENSOR_STATUS_LED: status_led.toggle()
  if USE_SENSOR_STATUS_LED: status_led.off()
#end main loop

