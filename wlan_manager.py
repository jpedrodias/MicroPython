# FILENAME: wlan_manager.py
import network, time, json

class WLAN_Manager():
  def __init__(self):
    self.file = 'wlan_manager.json'
    self.wlan = None
  
  def setup(self, ssid=None, password=None, append=False):
    self.mode(network.AP_IF)
    self.stop()
    self.mode(network.STA_IF)
    self.stop()
    
    if not ssid:
      ssid = input('WLAN SSID: ')
    if not password:
      password = input('password: ')
    if append:
      f = open(self.file, 'r')
      data = json.loads(f.read())
      f.close()
    else:
      data = {'wifi': []}
    
    if ssid and password:
      data['wifi'].append({'SSID': ssid, 'PASSWORD': password})
      f = open(self.file, 'w')
      f.write(json.dumps(data))
      f.close()
      del(f)
  #End setup
  
  def stop(self):
    if self.wlan:
      self.wlan.active(False)
      return not self.wlan.active()
    return True
  #End stop
  
  def start(self, ssid=None, password=None, attempts=20):
    # if not ssid or passowrd - get settings from file
    if not ssid and not password:
      try:
        f = open(self.file, 'r')
      except:
        f = None
        
      if not f:
        raise ValueError('{} file not found! Run .setup()'.format(self.file))
        
      data = json.loads(f.read())
      f.close()
      del(f)
    else:
      data = {"wifi": [{"SSID": ssid, "PASSWORD": password}]}
    # End if no json file is found       
    
    self.mode(network.STA_IF)
    if not self.wlan.active() or not self.wlan.isconnected():
      self.wlan.active(True)
      
      for cfg in data['wifi']:
        print('\nconnecting to:', cfg['SSID'], end=' ')
        if self.wlan.isconnected():
          break
        if cfg['SSID'] in self.wlan.scan():
          print(cfg['SSID'], 'not found.')
          continue
          
        self.wlan.connect(cfg['SSID'], cfg['PASSWORD'])
        for i in range( attempts + 5 ):
          if self.wlan.isconnected():
            break
          time.sleep(1)
          print('.', end='')
        if self.wlan.isconnected():
          break
    if self.wlan.isconnected():
      print('\nnetwork config:', self.wlan.ifconfig())
    else:
      print('\nnetwork connection failed')
      self.stop()
    return self.wlan.active( self.wlan.isconnected() )
  #End start
  
  def mode(self, mode=network.AP_IF):
    self.wlan = network.WLAN(mode)
    return True
  #End mode
  def check(self):
    if self.wlan:
      return self.wlan.active() and self.wlan.isconnected()
    else:
      return False
  #End check
#End class 

if __name__ == '__main__':
  wlan_client = WLAN_Manager()
  wlan_client.stop()
  time.sleep(2)
  #First time, use :
  #  wlan_client.setup()
  #  wlan_client.setup('HOME', 'password', append=False)
  #  wlan_client.setup('WORK', 'password', append=True)

  print('Setting wireless connecting')
  print('Changing mode wlan AP_IF:', wlan_client.mode(network.AP_IF))
  print('Stoping wlan AP mode:',  wlan_client.stop())
  sleep(1)
  
  print('Changing mode wlan STA_IF:', wlan_client.mode( network.STA_IF ))
  print('Stoping wlan STA mode:', wlan_client.stop() )
  sleep(1)
  
  print('Starting wlan in STA mode:', wlan_client.start() )
  print('Checking wlan:', wlan_client.check())
