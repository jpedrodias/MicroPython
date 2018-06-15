# MicroPython
Some tools to help when using MicroPython

<ul>
  <li>how to use wlan manager</li>
  <li>how to use mqtt manager</li>
  <li>how to use sensors manager</li>
</ul>



# wlan manager :: setup
Send wlan_manager.py to board using:
```
ampy -p /dev/ttyUSB0 put wlan_manager.py
```

The first time you need to run the `setup()` function. This function will creat the file wlan_manager.json to store SSID and password
```
from wlan_manager import *
wlan_client = WLAN_Manager()
wlan_client.setup()
wlan_client.start()
```

# wlan manager :: main loop example
```
# Connection to Wireless
from wlan_manager import *
wlan_client = WLAN_Manager()
sleep(1)
Done = False
while not Done:
  wlan_client.start()
  Done = wlan_client.check()
  led.toggle()
  sleep(1)
del(Done)
collect()
```

# mqtt manager :: setup
