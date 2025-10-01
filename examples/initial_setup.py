import network, time, mip

SSID = 'YOUR_SSID' # 2.4Gh
PASS = 'your-password'

wlan = network.WLAN(network.STA_IF)  
wlan.active(True)
wlan.connect(SSID, PASS) 

print("Waiting to connect:")
while not wlan.isconnected() and wlan.status() >= 0:
    print('.', end='')
    time.sleep(1)

print(wlan.ifconfig())

downloads = [
        'https://raw.githubusercontent.com/stlehmann/micropython-ssd1306/refs/heads/master/ssd1306.py',
        'https://raw.githubusercontent.com/jpedrodias/MicroPython/refs/heads/master/compiled/sensor_manager.mpy',
        'https://raw.githubusercontent.com/jpedrodias/MicroPython/refs/heads/master/compiled/wlan_manager.mpy',
        'https://raw.githubusercontent.com/jpedrodias/MicroPython/refs/heads/master/compiled/mqtt_manager.mpy',
        'https://raw.githubusercontent.com/jpedrodias/MicroPython/refs/heads/master/compiled/bme280.mpy',
        'https://raw.githubusercontent.com/jpedrodias/MicroPython/refs/heads/master/compiled/bmp085.mpy'
    ]

for file in downloads:
    mip.install(file)
    
print('All done!')
