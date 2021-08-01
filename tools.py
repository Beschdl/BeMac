import sys
import os
import pygame
import pygame.midi
import vgamepad as vg
import time

# Variablen

turnState = 0
gp = vg.VX360Gamepad()
turnSens = 120
turnBound = 32766/turnSens
lastClutch = 0


# Typical Midi Input: [[[176, 18, 59, 0], 1102288]] also i.read(1)[0][0][0,1,2,3]
# 0: Status
# 1: Channel
# 2: Value
# 3: ???, scheint immer 0 zu sien


# Activate Button, p/r=0/1, press or release
# inp will be the button, see class B

def act(pr, inp):
    if pr == 0:
        gp.press_button(button=inp)
    elif pr == 1:
        gp.release_button(button=inp)
    gp.update()
    print(str(pr) + "  " + str(inp))


class B:
    UP = 0x0001
    DOWN = 0x0002
    LEFT = 0x0004
    RIGHT = 0x0008
    START = 0x0010
    BACK = 0x0020
    LEFT_THUMB = 0x0040
    RIGHT_THUMB = 0x0080
    LEFT_SHOULDER = 0x0100
    RIGHT_SHOULDER = 0x0200
    GUIDE = 0x0400
    A = 0x1000
    B = 0x2000
    X = 0x4000
    Y = 0x8000


def check(read):
    print(read)
    channel = read[0][0][1]
    status = read[0][0][0]
    value = read[0][0][2]
    BTTN = 0x0000
    global turnState
    global lastClutch
    if (channel==24):
        if(value>63): # Aktualisieren
            turnState+=value-128
        elif(value<64):
            turnState+=value
        if(turnState<-turnBound): # Schauen ob OutOfBounds
            turnState = -turnBound
        elif(turnState>turnBound):
            turnState = turnBound
        gp.left_joystick(x_value=int(turnState*turnSens), y_value=0)
        print(turnState)
    if (status==144):
        if(channel==51): # start
            BTTN = B.START
        elif(channel==59): # zurück
            BTTN = B.BACK
        elif(channel==67): # stupid
            BTTN = B.GUIDE
        elif(channel==76): # Hupe
            BTTN = B.LEFT_THUMB
        elif(channel==72):
            BTTN = B.RIGHT_THUMB
        elif(channel==75):
            BTTN = B.A
        elif(channel==52):
            BTTN = B.Y
        elif(channel==48): # reset
            gp.reset()
            turnState = 0
        #Gedrückt/losgelassen?
        if (value==127):
            act(0, BTTN)
        elif (value==0):
            act(1, BTTN)
    if (status==176):
        if (channel==9): # Schaltung
            if (lastClutch == 0):
                if (value>125):
                    gp.press_button(B.X)
                    print("Switching Gears up")
                    lastClutch = 1
                elif(value<3):
                    gp.press_button(B.B)
                    print("Switching Gears down")
                    lastClutch = 1
            elif(lastClutch==1):
                if(value>20 and value<110):
                    lastClutch = 0
                    print("Switching Gears neutral")
                    gp.release_button(B.B)
                    gp.release_button(B.X)
        if (channel==11):   # Beschleunigung
            gp.right_trigger(value=(value*2))
        if (channel==12):   # Bremse
            gp.left_trigger(value=(value*2))
        if (channel==8):
            print()
    gp.update()
