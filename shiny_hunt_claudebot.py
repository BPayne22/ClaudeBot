from pynput.keyboard import Key, Controller
from getpixelcolor import pixel
import time
from math import isclose
import threading
import pytesseract
import cv2
import numpy as np
from PIL import ImageGrab
import requests
import re

# Claude Bot keyStrokes
keyboard = Controller()

# ClaudeBot Chat System using Ollama
chat_check_interval = 5  # seconds between OCR scans

# ClaudeBot prompt system
claude_system_prompt = (
    "You are ClaudeBot, a friendly Twitch stream assistant. The streamer is shiny hunting in Pokémon Black and White.\n"
    "Your job is to reply to viewers in Twitch chat. Only respond if the message clearly comes from a viewer in the format 'Username: message'.\n"
    "Never invent users, never continue a conversation unless the user sends a new message.\n"
    "Keep replies short (1 sentence max), casual, and Pokémon-themed. Do not roleplay or create stories.\n"
    "Always reply in English."
)

last_seen_message = ""

def grab_chat_text(region=(10, 500, 640, 600)):
    screenshot = ImageGrab.grab(bbox=region)
    gray = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
    text = pytesseract.image_to_string(gray)

    # Clean up artifacts like actual newlines, escaped \n, and OCR garbage
    text = (
        text
        .replace('\\n', ' ')        # literal \n from OCR
        .replace('\n', ' ')         # real newlines
        .replace('|', '')           # vertical bar artifacts
        .replace('\x0c', '')        # OCR end-of-text char
        .strip()
    )

    # Optional: collapse multiple spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

def extract_valid_line(text):
    # Search for a line that looks like 'Username: message'
    for line in text.splitlines():
        if re.match(r"^[A-Za-z0-9_]{3,20}: .+", line.strip()):
            return line.strip()
    return None

def generate_response(prompt):
    if not prompt:
        print("[ClaudeBot] Skipped invalid message: None or no match")
        return None
    try:
        resp = requests.post("http://localhost:11434/api/generate", json={
            "model": "mistral",
            "prompt": f"{claude_system_prompt}\n\nChat message: {prompt}\n\nClaudeBot:",
            "stream": False
        })

        if resp.status_code != 200:
            print(f"[ClaudeBot] API error: {resp.status_code} {resp.text}")
            return None

        data = resp.json()

        if "response" not in data:
            print("[ClaudeBot] Unexpected response format:", data)
            return None

        raw = data["response"].strip()
        reply = raw.split("\n")[0].strip()
        reply = reply.encode("ascii", errors="ignore").decode()

        if re.match(r"^[A-Za-z0-9_]+: ", reply):
            print("[ClaudeBot] Rejected hallucinated user reply:", repr(reply))
            return None

        return reply

    except Exception as e:
        print("ClaudeBot error:", e)
        return None


def claudebot_chat():
    global last_seen_message
    text = grab_chat_text()
    print("[OCR DEBUG]", repr(text))

    try:
        line = extract_valid_line(text)
    except Exception as e:
        print("[ClaudeBot] Error while extracting valid line:", e)
        return

    if line and line != last_seen_message:
        print("[ClaudeBot] Reading chat:", line)
        last_seen_message = line
        reply = generate_response(line)
        if reply:
            try:
                print("[ClaudeBot]", reply.encode('ascii', errors='replace').decode())
            except Exception as e:
                print("[ClaudeBot] Error printing reply:", e)

def start_claudebot():
    def loop():
        while True:
            claudebot_chat()
            time.sleep(chat_check_interval)
    threading.Thread(target=loop, daemon=True).start()

#######################################
import ctypes
SendInput = ctypes.windll.user32.SendInput

LeftReset = 0x10
RightReset = 0x11
START = 0x1c
SELECT = 0x36

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

#Button Controls    
def keyStrokeA():
    keyboard.press('x')
    time.sleep(.5)
    keyboard.release('x')

def keyStrokeB():
    keyboard.press('z')
    time.sleep(.5)
    keyboard.release('z')

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

# === Start ClaudeBot Thread ===
start_claudebot()

# === Main Loop ===
while shinyHunting == True:
    time.sleep(2)
    print("Lets get a Shiny!")

    print("Clearing Menu")
    menuMashCount = 0
    clearMenuMash(menuMashCount)

    print("Saftey Spam")
    bSpamCount = 0
    bSpam(bSpamCount)

    print("Speaking to Baddie")
    keyStrokeA()
    time.sleep(.1)
    keyStrokeA()
    time.sleep(3)

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

    print("Starting Mashing!")
    textMashCount = 0
    textMash(textMashCount)

    print("Opening Pokedex Menu")
    keyStrokeX()
    time.sleep(1.5)
    keyStrokeA()
    time.sleep(1.5)
    keyStrokeA()
    time.sleep(1.5)
    keyStrokeA()

    print("Is it Shiny?")
    time.sleep(1.5)
    isItShiny()
