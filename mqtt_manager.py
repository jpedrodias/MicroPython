# FILENAME: mqtt_manager.py
from umqtt.simple import MQTTClient
#from mqtt.robust import MQTTClient

class MQTT_Manager(MQTTClient):
  def __init__(self):
    from ubinascii import hexlify
    from machine import unique_id
    from ujson import loads
    from os import uname, listdir
    
    chip_name = uname().sysname
    chip_uid  = hexlify( unique_id() ).decode('utf-8')
    
    if  "mqtt_manager.json" not in listdir():
      self.setup()
      
    with open('mqtt_manager.json', 'r') as f:
      self.CONFIG = loads(f.read())
    
    self.CONFIG['client_id'] = '{}_{}'.format( chip_name, chip_uid )
    self.CONFIG['keepalive'] = 3600 # required for mosquitto v2
    
    args = {
      'server': self.CONFIG['broker'],
      'port': self.CONFIG['port'],
      'ssl': self.CONFIG['ssl'],
      'user': self.CONFIG.get('username', 'iot'),
      'password': self.CONFIG.get('password', 'iot'),
      'keepalive': self.CONFIG['keepalive']
    }
    if self.CONFIG.get('ssl', False):
      args['ssl_params'] = {
    }

    self.broker = MQTTClient(self.CONFIG['client_id'], **args)
  
  def setup(self):
    with open("mqtt_manager.json", "w") as f:
      f.write("""{
  "broker": "broker.hivemq.com",
  "port": 1883,
  "ssl": false,
  "username": "iot",
  "password": "iot",
  "delay": 60,
  "chatty": 1,
  "client_id": "?",
  "topic_debug" : "debug",
  "topic_status" : "devices/{device_id}/status",
  "topic_control" : "devices/{device_id}/control"
}
""")
    return True
  def get_topic(self, topic):
    if not topic:
      key = 'debug'
    else:
      key = 'topic_' + topic
    if key in self.CONFIG:
      return self.CONFIG[ key ].format( device_id=self.CONFIG[ 'client_id'] )
    else:
      return topic
  
  def check(self):
    try:
      self.broker.connect()
    except:
      print('Error MQTT check')
      return False
    return True
  
  def send(self, topic, msg):
    try:
      self.broker.publish( self.get_topic( topic ), bytes( msg, 'utf-8') )
    except:
      print('Error MQTT send')
      return False
    return True
    
  def check_msg(self):
    try:
      self.broker.check_msg()
    except:
      print('Error MQTT check_msg')
      return False
    return True
    
  def close(self):
    try:
      self.broker.disconnect()
    except:
      print('Error MQTT close')
      return False
    return True  

if __name__ == "__main__":
  mqtt_client = MQTT_Manager()
  print("MQTT config:")
  for i in mqtt_client.CONFIG:
    print("\t", i, ":", mqtt_client.CONFIG[i])

  TOPIC_SUB = mqtt_client.get_topic('control')
  TOPIC_PUB = mqtt_client.get_topic('status')

  mqtt_client.check()
  msgs = (
    'Connected to {} from {}'.format( mqtt_client.CONFIG['broker'] , mqtt_client.CONFIG['client_id'] ),
    'PUB {}'.format( TOPIC_PUB ),
    'SUB {}'.format ( TOPIC_SUB )
  )
  for msg in msgs:
    print(msg)
    mqtt_client.send('debug' , msg)
  del msgs
  
  #mqtt_client.close()
#end if main
