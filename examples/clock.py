from machine import RTC, Pin, I2C

import utime

from wlan_manager import WLAN_Manager
from board_manager import D1, D2
from ssd1306 import SSD1306_I2C

wlan_client = WLAN_Manager()
#wlan_client.setup('YOUR SSID', 'your password')
#wlan_client.start()

#import upip
#upip.install("urequests")
import urequests

web_query_delay = 3600000
retry_delay = 5000

i2c = I2C(scl=Pin(D1), sda=Pin(D2))
oled = SSD1306_I2C(128, 64, i2c, 0x3c)
rtc = RTC()


oled.fill(0)
oled.text('Loading Clock', 8, 40)
oled.show()

utime.sleep(1)

wlan_client.start()

oled.text('connection...', 0, 48)
oled.show()
utime.sleep(1)

oled.show()
utime.sleep(1)
for i in range(30):
  if wlan_client.check(): break
  oled.text('.', i * 8, 56)
  oled.show()
  utime.sleep(1)


url = "http://worldtimeapi.org/api/timezone/Europe/Lisbon"

# set timer
update_time = utime.ticks_ms() - web_query_delay

# main loop
while True:
    
  if not wlan_client.check():
    wlan_client.start()
  
  
  if utime.ticks_ms() - update_time >= web_query_delay:
    error_net = False
    try:
      response = urequests.get(url)
    except:
      error_net = True
    if not error_net or response.status_code == 200: # query success
  
      #print("JSON response:\n", response.text)
      
      # parse JSON
      parsed = response.json()
      datetime_str = str(parsed["datetime"])
      year = int(datetime_str[0:4])
      month = int(datetime_str[5:7])
      day = int(datetime_str[8:10])
      hour = int(datetime_str[11:13])
      minute = int(datetime_str[14:16])
      second = int(datetime_str[17:19])
      subsecond = int(round(int(datetime_str[20:26]) / 10000))
  
      # update internal RTC
      rtc.datetime((year, month, day, 0, hour, minute, second, subsecond))
      update_time = utime.ticks_ms()
      print("RTC updated\n")

    else: # query failed, retry retry_delay ms later
      update_time = utime.ticks_ms() - web_query_delay + retry_delay

  # generate formated date/time strings from internal RTC
  date_str = "Date: {1:02d}/{2:02d}/{0:4d}".format(*rtc.datetime())
  time_str = " Time: {4:02d}:{5:02d}:{6:02d}".format(*rtc.datetime())

  # update SSD1306 OLED display
  oled.fill(0)
  oled.text("*Robotica Clock*", 0, 4)
  oled.text(time_str, 0, 26)
  oled.text(date_str, 0, 56)
  oled.show()
  
  utime.sleep(0.5)
