# FILENAME: wlan_manager.py
from network import WLAN, AP_IF, STA_IF
from json import loads, dumps
        
class WLAN_Manager():
  def __init__(self):
    self.wlan = None
  
  def setup(self, ssid=None, password=None):
    self.mode(AP_IF)
    self.stop()
    self.mode(STA_IF)
    self.stop()
    
    if not ssid:
      ssid = input('WLAN SSID: ')
    if not password:
      password = input('password: ')
    
    if ssid and password:
      f = open('wlan_manager.json', 'w')
      f.write(dumps({'SSID': ssid, 'PASSWORD': password})) 
      f.close()
      del(f)
  
  def stop(self):
    if self.wlan:
      self.wlan.active(False)
      return not self.wlan.active()
    return True
  
  def start(self, ssid=None, password=None):
    if not ssid and not password:
      try:
        f = open('wlan_manager.json', 'r')
      except:
        f = None
    
      if f:
        cfg = loads(f.read())
      else:
        print('wlan configurations not found! Using default settings!')
        cfg = {'SSID': 'ATLANTICO', 'PASSWORD': 'oceano12'}
        self.setup(cfg['SSID'], cfg['PASSWORD'])
      del(f)
    #end if not ssid and password        
    
    self.mode(STA_IF)
    if not self.wlan.active() or not self.wlan.isconnected():
      self.wlan.active( True )
      print('connecting to:', cfg['SSID'])
      self.wlan.connect(cfg['SSID'], cfg['PASSWORD'])
      while not self.wlan.isconnected():
        pass
    
    print('network config:', self.wlan.ifconfig())
    return self.wlan.active()
  
  def mode(self, mode=AP_IF):
    self.wlan = WLAN(mode)
    return True
  
  def check(self):
    if self.wlan:
      return self.wlan.active() and self.wlan.isconnected()
    else:
      return False

if __name__ == '__main__':
  from time import sleep
    
  wlan_client = WLAN_Manager()
  #First time, use :
  #wlan_client.setup()
  
  print('Setting wireless connecting')
  print('Changing mode wlan AP_IF:', wlan_client.mode(AP_IF))
  print('Stoping wlan:',  wlan_client.stop())
  sleep(1)
  
  print('Changing mode wlan STA_IF:', wlan_client.mode( STA_IF ))
  print('Stoping wlan:', wlan_client.stop() )
  sleep(1)
    
  print('Starting wlan in STA mode:', wlan_client.start() )
  print('Checking wlan:', wlan_client.check())
  sleep(1)