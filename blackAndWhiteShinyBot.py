
from pynput.keyboard import Key, Controller
from getpixelcolor import pixel
import time
from math import isclose


#Claude Bot keyStrokes
keyboard = Controller()


#######################################
import ctypes

SendInput = ctypes.windll.user32.SendInput


LeftReset = 0x10
RightReset = 0x11
START = 0x1c
SELECT = 0x36

#arrowUp = 0xC8
#arrowDown = 0xD0
#arrowLeft = 0xCB
#arrowRight = 0xCD

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


# Actuals Functions
def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0,
                        ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


# directx scan codes
# http://www.gamespp.com/directx/directInputKeyboardScanCodes.html

#######################################
#Button Controls    
def keyStrokeA():
    keyboard.press('x')
    time.sleep(.5)
    keyboard.release('x')

def keyStrokeB():
    keyboard.press('z')
    time.sleep(.5)
    keyboard.release('z')
#Opens The Menu
def keyStrokeX(): 
    keyboard.press('s')
    time.sleep(.5)
    keyboard.release('s')

def keyStronkeY():
    keyboard.press('a')
    time.sleep(.5)
    keyboard.release('a')

def keyStrokeLeft():
    PressKey(LeftReset)
    time.sleep(.5)
    ReleaseKey(LeftReset)

def keyStrokeRight():
    PressKey(RightReset)
    time.sleep(.5)
    ReleaseKey(RightReset)

def keyStrokeStart():
    PressKey(START)
    time.sleep(.5)
    ReleaseKey(START)

def keyStronkeSelect(): 
    keyboard.press('2')
    time.sleep(.5)
    keyboard.release('2')

#Movement Controls
def stickPositionUp(): 
    keyboard.press('i')
    time.sleep(.5)
    keyboard.release('i')

def stickPositionDown():
    keyboard.press('k')
    time.sleep(.5)
    keyboard.release('k')

def stickPositionLeft():
    keyboard.press('j')
    time.sleep(.5)
    keyboard.release('j')

def stickPositionRight(): 
    keyboard.press('l')
    time.sleep(.5)
    keyboard.release('l')

#Soft Reset function
def softReset():
    print('SoftReset')
    PressKey(LeftReset)
    PressKey(RightReset)
    PressKey(START)
    PressKey(SELECT)
    time.sleep(1)
    ReleaseKey(LeftReset)
    ReleaseKey(RightReset)
    ReleaseKey(START)
    ReleaseKey(SELECT)

shinyHunting = True
textMashCount = 0
menuMashCount = 0
bSpamCount = 0

def textMash(textMashCount):
    while textMashCount < 13:   
        keyStrokeB()
        time.sleep(.1)
        keyStrokeB()
        time.sleep(.1)
        keyStrokeB()
        time.sleep(.1)
        textMashCount += 1

def clearMenuMash(menuMashCount):
    while menuMashCount < 10:
        keyStrokeA()
        time.sleep(1)
        menuMashCount += 1

def bSpam(bSpamCount):
    while bSpamCount < 5:
        keyStrokeB()
        time.sleep(1)
        bSpamCount += 1

def update_shiny_counter(file_path="counter.txt"):
    print("Updating Count")
    with open(file_path,'r') as f:
        count = int(f.read().strip())
        count += 1
    with open(file_path, 'w') as f:
        f.write(str(count))

red_star = (255,57,57)



def isItShiny():
    print("Well is it?")
    time.sleep(2)
    star_location_color = pixel(345,883)
    if star_location_color == red_star:
        print("Bro Its Shiny!")
        shinyHunting == False
    else:
        print("Looks Not Shiny")
        update_shiny_counter()
        softReset()



while shinyHunting == True:
    time.sleep(2)
    print("Lets get a Shiny!")
    #Starter Pokemon Check
    
    #Clear Main Menu
    print("Clearing Menu")
    menuMashCount = 0
    clearMenuMash(menuMashCount)
    
    #Safety B Spam
    print("Saftey Spam")
    bSpamCount = 0
    bSpam(bSpamCount)

    #Speak to Baddie
    print("Speaking to Baddie")
    keyStrokeA()
    time.sleep(.1)
    keyStrokeA()
    time.sleep(3)
    
    #Text mash to select starter
    keyStrokeB()
    time.sleep(1)
    keyStrokeB()
    time.sleep(1)
    keyStrokeB()
    time.sleep(1)
    print("Selecting Pokemon")
    time.sleep(4)
    print("moving Stick Now")
    keyStrokeB()
    stickPositionRight()
    stickPositionRight()
    time.sleep(.5)
    stickPositionRight()
    stickPositionRight()
    print("Oshawat hovered...")
    time.sleep(.3)
    keyStrokeA()
    time.sleep(1)
    keyStrokeA()
    time.sleep(1)

    #Text mash and deny nickname
    print("Starting Mashing!")
    textMashCount = 0
    textMash(textMashCount)
    
    #Open pokemon Menu
    print("Opening Pokedex Menu")
    keyStrokeX()
    time.sleep(1.5)
    keyStrokeA()
    time.sleep(1.5)
    keyStrokeA()
    time.sleep(1.5)
    keyStrokeA()
    
    #Run the colorCheck
    print("Is it Shiny?")
    time.sleep(1.5)
    isItShiny()
    
    