from time import sleep
from wlan_manager import WLAN_Manager
from mqtt_manager import MQTT_Manager

wlan_client = WLAN_Manager()
mqtt_client = MQTT_Manager()

def reconnect():
  wlan_client.start()
  success = wlan_client.check() and mqtt_client.check()
  if success:
    mqtt_client.broker.subscribe(TOPIC_SUB)
  return success

def mqtt_callback(topic, msg):
  print('MSG! Topic:{}; Data{}'.format(topic, msg))


TOPIC_SUB = mqtt_client.get_topic("control") # OUVIR
TOPIC_PUB = mqtt_client.get_topic("status")  # FALAR

chatty_client =  bool(mqtt_client.CONFIG.get("chatty", True))
mqtt_client.broker.set_callback(mqtt_callback)
print( "client_id:", mqtt_client.CONFIG["client_id"] )

connected = reconnect()
if connected:
  mqtt_client.send("debug", TOPIC_SUB)
  mqtt_client.send("debug", TOPIC_PUB)
  
i = 0
while True:
  i += 1
  print( "Sending: {}".format(i) )
  mqtt_client.send( TOPIC_PUB , "{}".format(i) )
  mqtt_client.check_msg()
  sleep(1)
