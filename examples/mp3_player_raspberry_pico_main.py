# filename: main.py
from dfplayermini import Player
from machine import Pin

from time import sleep

print("The MicroPython MP3 Player!!!")

NUM_SONGS = 2

player = Player(0, pin_TX=16, pin_RX=17)
#sleep(0.5)
#player.volume(20)

player_status, player_song = 0, 1

def manage_player():
    global player_status, player_song

    if player_status == 1:
        player_status = 0
        player.pause()
    else:        
        player_status = 1
        player.play(player_song)
  
def btn1_pressed(change):
    """Play and Pause"""
    manage_player()
    
def btn2_pressed(change):
    """Play Next Song"""
    global player_status, player_song
    player_song = (player_song % NUM_SONGS) + 1
    player_status = 0
    manage_player()

def btn3_pressed(change):
    """Play from Start"""
    global player_song
    player_song = 1
    manage_player()
    

btn1 = Pin(19, Pin.IN)
btn1.irq(handler=btn1_pressed, trigger=Pin.IRQ_FALLING)

btn2 = Pin(18, Pin.IN)
btn2.irq(handler=btn2_pressed, trigger=Pin.IRQ_FALLING)


#while True:
#    sleep(0.1)
