# sensor_bme280.py | main.py | v4
import micropython, machine, gc, time, json
from board_manager import D1, D2, D6

DEBUG = False  # Exit Infinit Loop if DEBUG is True
app_name = 'APP: MicroPython + MQTT + Sensor'
print( app_name )

def mqtt_callback(topic, msg):
  global chatty_client, main_delay
  if DEBUG: print(topic, msg)
  if msg == b'S':
    check_status(True)
  if msg == b'chatty on':
    chatty_client = True
  if msg == b'chatty off':
     chatty_client = False
  if msg.startswith(b'delay'):
    try:
      main_delay = int(msg.split()[1])
    except:
      pass

def check_status(publish=False):
  data = {'chatty': chatty_client, 'delay': main_delay}
  sensor.read() # Read from Sensor 
  for key, value in sensor.values_dict.items():
    data[key] = value
    print(key, '=', value, ';', end=' ')
  print()
  if publish:
    try:
      mqtt_client.send(TOPIC_PUB, json.dumps(data))
    except:
      print('MQTT send failed!')
  return True

class StatusLED():
  def __init__(self, pin):
    self.led = machine.Pin(pin, machine.Pin.OUT)
  def value(self, value):
    self.led.value(value)
  def on(self):
    self.value(1)
  def off(self):
    self.value(0)
  def toggle(self):
    self.led.value(not self.led.value())

def reconnect():
  wlan_client.start()
  success = wlan_client.check() and mqtt_client.check()
  if success:
    mqtt_client.broker.subscribe(TOPIC_SUB)
  return success
gc.collect()

led = StatusLED(D6)
led.on()

# Replace this lines with your sensor
i2c = machine.I2C(scl=machine.Pin(D1), sda=machine.Pin(D2)) # Pin 5 = D1 | Pin 4 = D2
from sensor_manager import Sensor_BME280
sensor = Sensor_BME280(i2c=i2c, address=0x77)
#End of sensor settings

from wlan_manager import WLAN_Manager
wlan_client = WLAN_Manager()

from mqtt_manager import MQTT_Manager
mqtt_client = MQTT_Manager()

TOPIC_SUB = mqtt_client.get_topic('control') # You talking to the sensor
TOPIC_PUB = mqtt_client.get_topic('status')  # The sensor talking to you
chatty_client =  bool(mqtt_client.CONFIG.get('chatty', True))
mqtt_client.broker.set_callback(mqtt_callback)
print( 'client_id:', mqtt_client.CONFIG['client_id'] )

connected = reconnect()
if DEBUG and connected:
  mqtt_client.send('debug', TOPIC_SUB)
  mqtt_client.send('debug', TOPIC_PUB)
  mqtt_client.send('debug', app_name)
gc.collect()

time.sleep(1)
if __name__ == '__main__':
  main_delay = mqtt_client.CONFIG['delay']
  if DEBUG: main_delay = 5
  Loops = 60
  gc.collect()
  while Loops:
    t_start = time.ticks_ms()
    gc.collect()
    if DEBUG: Loops -= 1
    led.on()
    if chatty_client:
      check_status(chatty_client and connected)
    while time.ticks_diff(time.ticks_ms(), t_start) <= main_delay * 1000:
      connected = mqtt_client.check_msg()
      if not connected:
        connected = reconnect()
        if not connected:
          connected = reconnect()
          time.sleep(4)
      led.toggle()
      time.sleep(0.5)
  #end loop
  mqtt_client.close()
  print(app_name)
  led.off()
  print('Rebooting')
  time.sleep(main_delay)
  machine.reset()
#end if __main__
