def init_setup(ssid, password):
  import network
  import time
  import mip
   
  wlan = network.WLAN(network.STA_IF)  
  wlan.active(True)
  wlan.connect(ssid, password) 
  
  while not wlan.isconnected() and wlan.status() >= 0:
    print("Waiting to connect:")
    time.sleep(1)

  print(wlan.ifconfig())
  
  print('Downloading umqtt.simple')
  mip.install('umqtt.simple', target='/')
  
  print('Downloading wlan_manager.mpy')
  mip.install('https://github.com/jpedrodias/MicroPython/raw/master/compiled/wlan_manager.mpy', target='/')
  
  print('Downloading mqtt_manager.mpy')
  mip.install('https://github.com/jpedrodias/MicroPython/raw/master/compiled/mqtt_manager.mpy', target='/')
  
if __name__ == "__main__":
  import time
  
  SSID_NAME = 'change this'
  SSID_PASSWORD = 'change this'
  init_setup(SSID_NAME, SSID_PASSWORD)
  
  print('WLAN Setup')
  from wlan_manager import WLAN_Manager
  wlan_client = WLAN_Manager()
  wlan_client.stop()
  time.sleep(1)
  wlan_client.setup(SSID_NAME, SSID_PASSWORD, append=False)
  time.sleep(1)
  wlan_client.start()
  
  print('MQTT Setup')
  from mqtt_manager import MQTT_Manager
  mqtt_client = MQTT_Manager()
  mqtt_client.setup()
  print(mqtt_client.get_topic('control'))
  print(mqtt_client.get_topic('status'))
