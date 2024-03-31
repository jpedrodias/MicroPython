from datetime import datetime
import sys

import signal
def signal_handler(signal, frame):
    global global_done
    print('You pressed Ctrl+C!')
    global_done = True
signal.signal(signal.SIGINT, signal_handler)


# connection to Serial Ports
from serial import Serial # pip install pyserial
from serial.tools.list_ports import comports

DEFAULT_OUTPUT_FILENAME = "Serial_Port_Reader.csv"

# Open connection to First Serial Port - Set speed to (9600 ou 112500)
serial_ports = comports()
if len(serial_ports) == 0:
    print('No serial ports found!')
    sys.exit()
elif len(serial_ports) == 1:
    serial_device = serial_ports[0]
    print(serial_device.description)
else:
    print('Select a Serial device:')
    print('0 - exit')
    for i, serial_device in enumerate(comports()):
        print(i+1, serial_device)
    
    done = False
    while not done:
        serial = input(': ')
        try:
            serial = int(serial)
            done = True
        except:
            serial = 0
            
        if serial == 0: sys.exit()
        serial_device = serial_ports[serial-1]
        
baudrates = [9600, 112500]
print('Select Baudrate:')
print('0 - exit')
for i, baudrate in enumerate(baudrates):
    print(i+1, baudrate)

done = False
while not done:
    baudrate = input(': ')
    try:
        baudrate = int(baudrate)
        done = True
    except:
        baudrate = 0
        done = False
    if baudrate == 0: sys.exit()
    baudrate = baudrates[baudrate-1]

serial_connection = Serial( serial_device.device, baudrate, timeout=1)


output_data_file = input('Input filename: ')
if not output_data_file:
    output_data_file = DEFAULT_OUTPUT_FILENAME


print( "Python Serial Port Reader" )
print()
print("Recording data in file:", output_data_file)
print("To Exit Press: Ctrl+C")


file = open(output_data_file, "w")

global_done = False
while not global_done:
    valor_lido = serial_connection.readline()
    valor_lido = valor_lido.strip()
    valor_lido = str( valor_lido,'utf-8' )
    
    if valor_lido:
        print( "%s; %s" % (datetime.now(), valor_lido) )    
        file.write( "%s; %s\n" % (datetime.now(), valor_lido) )

file.close()
print("Data saved to", output_data_file)
