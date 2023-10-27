import signal, sys


# connection to Serial Ports
from serial import Serial
from serial.tools.list_ports import comports as serial_ports

# Show system time
from datetime import datetime


def signal_handler(signal, frame):
    global Done
    print('You pressed Ctrl+C!')
    Done = True
signal.signal(signal.SIGINT, signal_handler)


Done = False
outputdatafile = "Serial_Port_Reader.csv"


print( "Python Serial Port Reader" )
print()
print("Recording data in file:", outputdatafile)
print("To Exit Press: Ctrl+C")


# Open connection to First Serial Port - Set speed to (9600 ou 112500)
serial_port = serial_ports()[0]
micro_Controller = Serial( serial_port.device, 112500, timeout=1)


file = open(outputdatafile, "w")

Done = False
while not Done:
    valor_lido = micro_Controller.readline()
    valor_lido = valor_lido.strip()
    valor_lido = str( valor_lido,'utf-8' )
    
    if valor_lido:
        print( "%s; %s" % (datetime.now(), valor_lido) )    
        file.write( "%s; %s\n" % (datetime.now(), valor_lido) )

file.close()
print("Data saved to", outputdatafile)
