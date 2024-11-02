from machine import Pin
from time import sleep
import network, socket, gc
gc.enable()

led = Pin(10, Pin.OUT)

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('SSID', 'password')

print('Connecting', end='')
while not wlan.isconnected():
    led.toggle()
    print('.', end='')
    sleep(1)
print()
    
addr = (wlan.ifconfig()[0], 80)
s = socket.socket()
s.bind(addr)
s.listen(1)

print('Listening for connections on', addr)
html_body = '''
<html>
<head><title>Control LED</title></head>
<body>
<h1>{}</h1>
    <a href="/ON">Turn LED ON</a>
    <a href="/OFF">Turn LED OFF</a>
</body>
</html>
'''

led_status = {0: 'OFF', 1: 'ON'}
try:
    while True:
        cl, addr = s.accept()
        print('Client connected from', addr)
        request = cl.recv(1024)
        request = str(request)
        print('Request:', request)
        if '/favicon.ico' in request:
            cl.close()
            continue
            
        if 'GET /ON ' in request:
            value = 1
        elif 'GET /OFF ' in request:
            value = 0
        else:
            value = led.value()
        
        led.value(value)
        response = led_status.get(value)
        response = 'LED is ' + response
        
        cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
        cl.send(html_body.format(response))
        cl.close()
        
        gc.collect()
except Exception as e:
    print('Error:', e)
finally:
    s.close()
    wlan.active(False)
  
