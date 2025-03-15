import pyautogui
import time
import keyboard
import sys

countdowntime = 5
clickon = True
clicking = True
howtouse = """To use this autoclicker, move the cursor to 
where you want to click. Press e to stop 
clicking, and press w to start clicking 
again. To close the program, press q. 
The -m flag removes this message. The -c 
flag makes the default mode not to be clicking. """
showmanual = True

def countdown(sec):
    i = -1
    while i < sec:
        time.sleep(1)
        i += 1 
        print(f"{sec-i}")

def commandlineargs():
    global clicking, showmanual, countdowntime, howtouse
    if "-c" in sys.argv: clicking = False
    if "-f" in sys.argv: showmanual = False
    if showmanual: print(howtouse)

commandlineargs()
countdown(countdowntime)

while clickon:
    if clicking: pyautogui.click()
    if keyboard.is_pressed("e"): clicking = False 
    if keyboard.is_pressed("w"): clicking = True
    clickon = not(keyboard.is_pressed("q"))