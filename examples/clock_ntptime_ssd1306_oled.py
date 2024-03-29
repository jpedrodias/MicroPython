from machine import Pin, I2C, RTC
import time, ntptime

# Hardware connection to i2c 
from board_manager import D1, D2
i2c = I2C(scl=Pin(D1), sda=Pin(D2))

# Hardware connection to oled display
from ssd1306 import SSD1306_I2C
ssd = SSD1306_I2C(128, 64, i2c, 0x3c)
rtc = RTC()

# wireless connection
from wlan_manager import WLAN_Manager
wlan_client = WLAN_Manager()

# SETTINGS
ntptime.host = 'ntp02.oal.ul.pt' # Portugal
web_query_delay = 3600000 # 1h
retry_delay = 5000

# Screen 0: Booting
ssd.fill(0)
ssd.text('Booting...', 4, 8)
ssd.text('ntp server:', 0, 16)
ssd.text(ntptime.host , 0, 24)
ssd.show()
time.sleep(1)

# Start Wireless connection
ssd.text('wireless...', 0, 32)
ssd.show()
wlan_client.start()
time.sleep(1)

# set timer
update_time = time.ticks_ms() - web_query_delay

# main loop
while True:
  if time.ticks_ms() - update_time >= web_query_delay:
    if not wlan_client.check():
      wlan_client.start()
      
    error_net = False
    try:
      ntptime.settime()
    except:
      error_net = True
    
    if not error_net:
      try:
          t = time.localtime()
      except:
          continue
    
      year, month, day = t[0], t[1], t[2]
      hour, minute, second = t[3], t[4], t[5]
      subsecond = t[6]
  
      #update internal RTC
      rtc.datetime((year, month, day, 0, hour, minute, second, subsecond))
      update_time = time.ticks_ms()
      print("RTC updated\n")

    else: # query failed, retry retry_delay ms later
      update_time = time.ticks_ms() - web_query_delay + retry_delay
      
    # if not error_net
    
  # generate formated date/time strings from internal RTC
  date_str = "Date: {2:02d}/{1:02d}/{0:4d}".format(*rtc.datetime())
  time_str = " Time: {4:02d}:{5:02d}:{6:02d}".format(*rtc.datetime())

  # update SSD1306 OLED display
  ssd.fill(0)
  ssd.text(time_str, 0, 26)
  ssd.text(date_str, 0, 56)
  ssd.show()
  
  time.sleep(0.5)
