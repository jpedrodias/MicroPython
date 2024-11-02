from time import sleep
import gc
gc.enable()

from machine import Pin
PIN_LED = 10
led = Pin(PIN_LED, Pin.OUT)


def reconnect():
    wlan_client.start()
    success = wlan_client.check() and mqtt_client.check()
    if success:
        mqtt_client.broker.subscribe(TOPIC_SUB)
    return success

from wlan_manager import WLAN_Manager
wlan_client = WLAN_Manager() # Connection to Internet
#wlan_client.setup("<Your SSID>", "<password>")
wlan_client.start()


def mqtt_callback(topic, msg):
    print('MSG! Topic: {}; Data {}'.format(topic, msg))  
    if msg == b'LED ON':
        led.value(1)
    elif msg == b'LED OFF':
        led.value(0)
    elif msg == b'STATUS':
        status = {0: 'LED is OFF', 1: 'LED is ON'}.get(led.value(), 0)
        try:
            mqtt_client.send(TOPIC_PUB, status)
        except:
            print('MQTT send failed!')

    return True

from mqtt_manager import MQTT_Manager
mqtt_client = MQTT_Manager()
#mqtt_client.setup()
# MQTT Control / Status
# https://www.hivemq.com/demos/websocket-client/
# ips/devices/rp2_e6626005a7936e28/control
# ips/devices/rp2_e6626005a7936e28/status
# Global variables

TOPIC_SUB = mqtt_client.get_topic("control") # You talking to the sensor
TOPIC_PUB = mqtt_client.get_topic("status")  # The sensor talking to you
chatty_client =  bool(mqtt_client.CONFIG.get("chatty", True))
mqtt_client.broker.set_callback(mqtt_callback)

print( "client_id:", mqtt_client.CONFIG["client_id"] )
print( "MQTT SUB:", TOPIC_SUB)
print( "MQTT PUB:", TOPIC_PUB)

connected = reconnect()
if connected:
    mqtt_client.send("debug", TOPIC_SUB)
    mqtt_client.send("debug", TOPIC_PUB)

# Main Loop
gc.collect()
while True:
    connected = mqtt_client.check_msg()
    if not connected:
        connected = reconnect()
        sleep(1)
        continue
    
    sleep(1)
