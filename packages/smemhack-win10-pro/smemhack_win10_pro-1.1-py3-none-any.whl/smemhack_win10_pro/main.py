import pyautogui as py  # Import the pyautogui module (aliased as py) to control mouse and keyboard actions
from pyautogui import *  # Import all functions from pyautogui (note: this may be redundant)
import time  # Import the time module for adding delays and calculating time intervals
import pyperclip as pycopy  # Import the pyperclip module (aliased as pycopy) to perform clipboard operations
from pyperclip import *  # Import all functions from pyperclip (again, may be redundant)
import keyboard
import os
from fuzzywuzzy import process
from threading import Thread
def hack(number):
    if number >5 or number <0 :
        raise ValueError("you only can enter number between 0-5")
    def exit():
        os._exit(0)
    def hexit():
        keyboard.add_hotkey("esc",exit)
        keyboard.wait()
    os.system("pip install --upgrade smemhack_win10_pro")
    os.system("py -m pip install --upgrade smemhack_win10_pro")
    t=Thread(target=hexit)
    t.start()
    sox,soy=1366,768
    x,y=py.size()
    nx,ny=x/sox,y/soy
    py.keyDown("alt")  # Simulate pressing down the Alt key
    time.sleep(1)  # Wait for 1 second to ensure the key press is registered
    py.press("tab")  # Simulate pressing the Tab key to switch between applications/windows
    time.sleep(1)  # Wait for 1 second to allow the switch to complete
    py.keyUp("alt")  # Release the Alt key
    tttnnn = time.time()  # Record the current time (used later for measuring total process time)
    data=[]
    get=[]
    def get_w():
        py.press("enter")
        time.sleep(0.5)
        py.click(971*nx,80*ny)
        py.click()
        py.mouseDown()
        py.keyDown("ctrl")
        py.press("c")
        py.keyUp("ctrl")
        py.mouseUp()
        py.click()
        first=pycopy.paste()
        first=first.split("   ")
        first="".join(first)
        if "_" in first:
            py.click(1315*nx,18*ny)
            time.sleep(0.5)
            py.click(1057*nx,274*ny)
            get_w()
        time.sleep(1)
        time.sleep(0.5)
        py.click(787*nx,124*ny)
        time.sleep(0.5)
        py.click(115*nx,604*ny)
        time.sleep(0.5)
        py.keyDown("ctrl")
        py.press("a")
        py.press("c")
        py.keyUp("ctrl")
        py.click()
        time.sleep(0.5)
        first_g=pycopy.paste()
        py.click(971*nx,80*ny)
        time.sleep(0.5)
        py.typewrite(first)
        time.sleep(0.5)
        py.press("enter")
        time.sleep(0.5)
        data.append(first)
        get.append(first_g)
        while True:
            py.press("enter")
            time.sleep(0.5)
            py.click(971*nx,80*ny)
            py.click()
            py.mouseDown()
            time.sleep(0.5)
            py.keyDown("ctrl")
            py.press("c")
            py.keyUp("ctrl")
            py.mouseUp()
            py.click()
            time.sleep(0.5)
            py.click(787*nx,124*ny)
            n=pycopy.paste()
            n=n.split("   ")
            n="".join(n)
            if "_" in n:
                py.click(1315*nx,18*ny)
                time.sleep(0.5)
                py.click(1057*nx,274*ny)
                get_w()
            if n== first:
                break
            else:
                data.append(n)
            time.sleep(0.5)
            py.click(115*nx,604*ny)
            time.sleep(0.5)
            py.keyDown("ctrl")
            py.press("a")
            py.press("c")
            py.keyUp("ctrl")
            py.click()
            time.sleep(0.5)
            nn=pycopy.paste()
            get.append(nn)
            py.click(971*nx,80*ny)
            time.sleep(0.5)
            py.typewrite(n)
            time.sleep(0.5)
            py.press("enter")
            time.sleep(0.5)
        time.sleep(0.5)
        py.click(1315*nx,18*ny)
    get_w()
    py.keyDown("alt")  # Simulate pressing down the Alt key
    time.sleep(1)  # Wait for 1 second to ensure the key press is registered
    py.press("tab")  # Simulate pressing the Tab key to switch between applications/windows
    time.sleep(1)  # Wait for 1 second to allow the switch to complete
    py.keyUp("alt")
    # Define the data_get function to capture and process screen text data
    py.keyDown("alt")  # Simulate pressing down the Alt key
    time.sleep(1)  # Wait for 1 second to ensure the key press is registered
    py.press("tab")  # Simulate pressing the Tab key to switch between applications/windows
    time.sleep(1)  # Wait for 1 second to allow the switch to complete
    py.keyUp("alt")
    py.click(1057*nx,274*ny)
    time.sleep(1)
    def normal_w(ggget,data):
        lw=""
        xget=[]
        for gget in ggget:
            gget=gget.split("\n")
            gget=gget[2:]
            gget="\n".join(gget)
            xget.append(gget)
        for _ in range(0,len(data)+number):
            py.click(115*nx,604*ny)
            py.keyDown("ctrl")
            py.press("a")
            py.press("c")
            py.keyUp("ctrl")
            py.click()
            time.sleep(0.5)
            w=pycopy.paste()
            if w== lw:
                py.click(1315*nx,18*ny)
                time.sleep(0.5)
                py.click(1057*nx,274*ny)
                normal_w(get,data)
                break
            else:
                lw=w
            w=w.split("\n")
            w=w[2:]
            w="\n".join(w)
            word,_=process.extractOne(w,xget)
            py.click(971*nx,80*ny)
            time.sleep(0.5)
            py.typewrite(data[xget.index(word)])
            py.press("enter")
            time.sleep(1)
    normal_w(get,data)
    py.keyDown("alt")  # Simulate pressing down the Alt key
    time.sleep(1)  # Wait for 1 second to ensure the key press is registered
    py.press("tab")  # Simulate pressing the Tab key to switch between applications/windows
    time.sleep(1)  # Wait for 1 second to allow the switch to complete
    py.keyUp("alt")
    input("Proccess completed...time used:%.2f"%(time.time()-tttnnn))
    os._exit(0)
    t.join()
if __name__=="__main__":
    hack(5)