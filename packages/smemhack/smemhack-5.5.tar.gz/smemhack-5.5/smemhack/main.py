import pyautogui as py  # Import the pyautogui module (aliased as py) to control mouse and keyboard actions
from pyautogui import *  # Import all functions from pyautogui (note: this may be redundant)
import time  # Import the time module for adding delays and calculating time intervals
import pyperclip as pycopy  # Import the pyperclip module (aliased as pycopy) to perform clipboard operations
from pyperclip import *  # Import all functions from pyperclip (again, may be redundant)
import json  # Import the json module for reading and writing JSON files
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense,LSTM,Embedding,Dropout,Flatten
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.regularizers import l2
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import numpy as np
def hack():
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
        py.click(906*nx,106*ny)
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
        time.sleep(0.5)
        py.click(773*nx,157*ny)
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
        py.click(906*nx,106*ny)
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
            py.click(906*nx,106*ny)
            py.click()
            py.mouseDown()
            time.sleep(0.5)
            py.keyDown("ctrl")
            py.press("c")
            py.keyUp("ctrl")
            py.mouseUp()
            py.click()
            time.sleep(0.5)
            py.click(797*nx,156*ny)
            n=pycopy.paste()
            n=n.split("   ")
            n="".join(n)
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
            py.click(906*nx,106*ny)
            time.sleep(0.5)
            py.typewrite(n)
            time.sleep(0.5)
            py.press("enter")
            time.sleep(0.5)
        time.sleep(0.5)
        py.click(1316*nx,54*ny)
    get_w()
    py.keyDown("alt")  # Simulate pressing down the Alt key
    time.sleep(1)  # Wait for 1 second to ensure the key press is registered
    py.press("tab")  # Simulate pressing the Tab key to switch between applications/windows
    time.sleep(1)  # Wait for 1 second to allow the switch to complete
    py.keyUp("alt")
    # Define the data_get function to capture and process screen text data
    model=Sequential([
        Embedding(input_dim=100,output_dim=50,input_length=5),
        LSTM(128),
        Dense(64,activation="relu"),
        Dense(len(data),activation="softmax")
    ])
    model.compile(optimizer="adam",
                  loss="sparse_categorical_crossentropy",
                  metrics=["accuracy"])
    y=np.array(list(range(0,len(data))))
    tokenizer=Tokenizer(num_words=100)
    tokenizer.fit_on_texts(get)
    x=tokenizer.texts_to_sequences(get)
    x=pad_sequences(x,maxlen=5)
    model.fit(x,y,epochs=100,batch_size=1)
    py.keyDown("alt")  # Simulate pressing down the Alt key
    time.sleep(1)  # Wait for 1 second to ensure the key press is registered
    py.press("tab")  # Simulate pressing the Tab key to switch between applications/windows
    time.sleep(1)  # Wait for 1 second to allow the switch to complete
    py.keyUp("alt")
    py.click(1053*nx,317*ny)
    time.sleep(1)
    lw=""
    def normal_w():
        get=get.split("\n")
        get=get[2:]
        get="\n".join(get)
        for _ in range(0,len(data)+5):
            py.click(115*nx,604*ny)
            py.keyDown("ctrl")
            py.press("a")
            py.press("c")
            py.keyUp("ctrl")
            py.click()
            time.sleep(0.5)
            w=pycopy.paste()
            w=w.split("\n")
            w=w[2:]
            w="\n".join(w)
            for x in get:
                if w==x:
                    py.click(906*nx,106*ny)
                    time.sleep(0.5)
                    py.typewrite(data[get.index(x)])
                    py.press("enter")
                    time.sleep(1)
    for _ in range(0,len(data)+5):
        py.click(115*nx,604*ny)
        py.keyDown("ctrl")
        py.press("a")
        py.press("c")
        py.keyUp("ctrl")
        py.click()
        time.sleep(0.5)
        gg=pycopy.paste()
        if gg== lw:
            py.click(1316*nx,54*ny)
            time.sleep(0.5)
            py.click(1053*nx,317*ny)
            normal_w()
            break
        else:
            lw=gg
        gg=[gg]
        gg=tokenizer.texts_to_sequences(gg)
        gg=pad_sequences(gg,maxlen=5)
        prediction=model.predict(gg)
        pd=np.argmax(prediction)
        py.click(906*nx,106*ny)
        time.sleep(0.5)
        py.typewrite(data[pd])
        py.press("enter")
        time.sleep(1)
    py.keyDown("alt")  # Simulate pressing down the Alt key
    time.sleep(1)  # Wait for 1 second to ensure the key press is registered
    py.press("tab")  # Simulate pressing the Tab key to switch between applications/windows
    time.sleep(1)  # Wait for 1 second to allow the switch to complete
    py.keyUp("alt")
    input("Proccess completed...time used:%.2f"%(time.time()-tttnnn))

