from machine import Pin, ADC
from time import ticks_ms, ticks_us, ticks_cpu, sleep, sleep_us
from gc import mem_free, collect
collect()

def change_trigger(pin):
    global TRIGGER
    TRIGGER = True


# Settings and memory allocation
BUFFER_SIZE = 10000  # Limited by amount of RAM
TRIGGER = False      # Not a constante but a GLOBAL
buffer_data = [0 for _ in range(BUFFER_SIZE)]
buffer_time = [0 for _ in range(BUFFER_SIZE)]

# STEP 0: Hardware configurations
adc = ADC(0)
adc.atten(ADC.ATTN_11DB) # 
# ADC.ATTN_0DB    : No attenuation (100mV - 950mV)
# ADC.ATTN_2_5DB  : 2.5dB attenuation (100mV - 1250mV)
# ADC.ATTN_6DB    : 6dB attenuation (150mV - 1750mV)
# ADC.ATTN_11DB   : 11dB attenuation (150mV - 2450mV)

adc.width(ADC.WIDTH_12BIT)
# ADC.WIDTH_9BIT  : range 0 to 511
# ADC.WIDTH_10BIT : range 0 to 1023
# ADC.WIDTH_11BIT : range 0 to 2047
# ADC.WIDTH_12BIT : range 0 to 4095

trigger = Pin(2, Pin.IN)
sleep_us(10)
trigger.irq(handler=change_trigger, trigger=Pin.IRQ_FALLING)
#trigger.irq(handler=change_trigger, trigger=Pin.IRQ_RISING) # depends on sensor
sleep_us(10)


#STEP 1: Calibration - get background noise
print("Caligration")
BACKGROUND_NOISE = 0
for i in range(BUFFER_SIZE):
    buffer_data[i] = adc.read_u16()
    if buffer_data[i] > BACKGROUND_NOISE:
        BACKGROUND_NOISE= buffer_data[i]
    sleep_us(1)
#BACKGROUND_NOISE = 0

# STEP 2: Wait for trigger - IRQ on signal (voltage from sensor) FALLING
print("Waiting for release")
#while TRIGGER==False:
#    pass


# STEP 3: Second waiting while below noise levels
#while adc.read_u16() < BACKGROUND_NOISE:
#    pass


# STEP 4: Active recording
buffer_time[0] = ticks_us()
for i in range(BUFFER_SIZE):
    buffer_data[i] = adc.read_u16()
    buffer_time[i] = ticks_us()
    #sleep_us(1) # Use this if the event duration is longer than the buffer
#buffer_time[-1] = ticks_us()

max_read = max(buffer_data)
print('Valor lido:', max_read)


# STEP 5: Dump data to Serial Port
from json import dumps
for i in range(BUFFER_SIZE):
    break
    data = {
        'i': i,
        'time': buffer_time[i],
        'data': buffer_data[i]
    }
    payload = dumps(data)
    print(payload)

data = {
    'time_i': buffer_time[0],
    'data_i': buffer_data[0],
    'time_f': buffer_time[-1],
    'data_f': buffer_data[-1],
}
payload = dumps(data)
print(payload)

total_time = buffer_time[-1] - buffer_time[0]
print("Reading time:", total_time, total_time // 1000 )

