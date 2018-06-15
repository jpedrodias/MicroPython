# MicroPython
Some tools to help when using MicroPython

<ul>
  <li>how to use wlan manager</li>
  <li>how to use mqtt manager</li>
  <li>how to use sensors manager</li>
</ul>



# wlan manager :: setup
```
from wlan_manager import *
wlan_client = WLAN_Manager()
wlan_client.setup()
wlan_client.start()

```

# wlan manager :: main loop
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
