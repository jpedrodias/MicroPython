# atuador_relays1.py | main.py | v4
import micropython, machine, gc, time, json
from board_manager import D1, D2

DEBUG = micropython.const(0)  # Exit Infinit Loop if DEBUG is True
app_name = 'RelayBoard v4'
print( app_name )

# Connection to Slave Arduino
i2c = machine.I2C(scl=machine.Pin(D1), sda=machine.Pin(D2))
i2c_slave = micropython.const(8) #i2c.scan()[0]
i2c_cmds = [b'O*', b'C*', b'L*', b'O1', b'C1', b'L1', b'O2', b'C2', b'L2']

def mqtt_callback(topic, msg):
  global chatty_client, main_delay
  if DEBUG: print(topic, msg)
  if msg == b'S':
    check_status(True)
  elif msg == b'chatty on':
    chatty_client = True
  elif msg == b'chatty off':
     chatty_client = False
  elif msg.startswith(b'delay'):
    try:
      main_delay = int(msg.split()[1])
    except:
      pass
  elif msg in i2c_cmds:
    i2c.writeto(i2c_slave, msg)

def check_status(publish=False):
  status = i2c.readfrom(i2c_slave, 6)
  status_str = ''
  for c in status:
    status_str += str(c)
  if DEBUG: print(status_str)
  data = {
    'chatty': chatty_client,
    'delay' : main_delay,
    'status': status_str
  }
  if publish:
    try:
      mqtt_client.send(TOPIC_PUB, json.dumps(data))
    except:
      print('MQTT send failed!')
  print('MQTT', data)

def reconnect():
  wlan_client.start()
  print("MQTT check...")
  success = wlan_client.check() and mqtt_client.check()
  if success:
    mqtt_client.broker.subscribe(TOPIC_SUB)
  return success
gc.collect()

from wlan_manager import WLAN_Manager
wlan_client = WLAN_Manager()

from mqtt_manager import MQTT_Manager
mqtt_client = MQTT_Manager()
TOPIC_SUB = mqtt_client.get_topic('control')
TOPIC_PUB = mqtt_client.get_topic('status')
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
if __name__ == "__main__":
  main_delay = mqtt_client.CONFIG['delay']
  if DEBUG: main_delay = 5
  Loops = 60
  gc.collect()
  while Loops:
    t_start = time.ticks_ms()
    if DEBUG: Loops -= 1
    gc.collect()
    if chatty_client:
      check_status(chatty_client and connected)
    while time.ticks_diff(time.ticks_ms(), t_start) <= main_delay * 1000:
      connected = mqtt_client.check_msg()
      if not connected:
        connected = reconnect()
        if not connected:
          time.sleep(5)
      time.sleep(0.5)
  #end loop
  mqtt_client.close()
  print(app_name)
  print( "Rebooting" )
  time.sleep(5)
  machine.reset() 
#end if __main__
