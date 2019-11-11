import tkinter as tk
from urllib.request import urlopen
# import base64
import json
import random
import webbrowser
import tkinter.ttk
from PIL import ImageTk, Image
from io import BytesIO

#Get number of latest comic
info = json.loads(urlopen("https://xkcd.com/info.0.json").read())
currentnum = maxnum = info["num"]

#Load and display comic
def loadimage(comicnum):

    #Update current comic number
    global currentnum
    currentnum = comicnum

    #Get comic info from API
    global info
    info = json.loads(urlopen(f"https://xkcd.com/{comicnum}/info.0.json").read())

    #Set alt text, title and transcript
    try:
        alt_var.set(info["alt"])
    except:
        alt_var.set("cannot show alt text")
    try:
        title_var.set(str(info["num"]) + ": " + info["title"])
    except:
        title_var.set("Cannot show title")
    transcript_var.set("")

    #Download image
    img_url = info["img"]
    img_data = urlopen(img_url).read()
    image = Image.open(BytesIO(img_data))

    #Scale image
    width, height = image.size
    if width > height:
        newwidth = 800
        newheight = int(height/width*800)
    else:
        newheight = 700
        newwidth = int(width/height*700)
    image = image.resize((newwidth, newheight), Image.ANTIALIAS)

    #Display image
    image = ImageTk.PhotoImage(image)
    panel.configure(image=image)
    panel.image = image


#Go to previous comic
def getPrev():
    global currentnum
    global maxnum
    if currentnum == 1:
        currentnum = maxnum
    else:
        currentnum -=1
    loadimage(currentnum)

#Go to next comic
def getNext():
    global currentnum
    global maxnum
    if currentnum < maxnum:
        currentnum +=1
    else:
        currentnum = 1
    loadimage(currentnum)

#Go to random comic
def getRandom():
    global currentnum
    global maxnum
    currentnum = random.randint(1, maxnum)
    loadimage(currentnum)

#Show comic transcript
def showTranscript():
    global info
    transcript = info["transcript"]
    if transcript == "":
        transcript = "No transcript available"
    try:
        transcript_var.set(transcript)
    except:
        transcript_var.set("Cannot show transcript")

#Go to comic number
def goToNum(event=0):
    entry = int(int_box.get())
    int_box.delete(0, tk.END)
    global currentnum
    global maxnum
    if entry <= currentnum and entry > 0:
        currentnum = entry
    elif entry <= 0:
        currentnum = 1
    else:
        currentnum = maxnum
    loadimage(currentnum)

#Setup
window = tk.Tk()
window.title("xkcd")

#Configure columns
window.columnconfigure((0,1,2,5,6,7), weight = 4)
window.columnconfigure(3, weight=3)
window.columnconfigure(4, weight=1)

#Create buttons
bt_first = tk.Button(window, text = "<<",command = lambda: loadimage(1)).grid(row=0, column=0, sticky = "WE")
bt_prev = tk.Button(window, text = "Previous", command = getPrev).grid(row=0, column=1, sticky = "WE")
bt_random = tk.Button(window, text = "Random", command = getRandom).grid(row=0, column=2, sticky = "WE")

#Create input box and go button
int_box = tk.Entry(window)
int_box.grid(row=0, column=3, sticky="WE", padx=2)
int_box.insert(0, str(currentnum))
int_box.bind('<Return>', goToNum) 
bt_goto = tk.Button(window, text = "Go", command = goToNum).grid(row=0, column=4, sticky="WE")

#Create options menu
menubutton = tk.Menubutton(window, text = "Options", relief="raised", bd=2)
menubutton.grid(row=0, column=5, sticky = "NESW")
menubutton.menu = tk.Menu(menubutton)
menubutton["menu"]=menubutton.menu
menubutton.menu.add_command(label = "Explain", command = lambda: webbrowser.open(f"www.explainxkcd.com/{currentnum}"))
menubutton.menu.add_command(label = "Original", command = lambda: webbrowser.open(f"www.xkcd.com/{currentnum}"))
menubutton.menu.add_command(label = "Transcript", command = showTranscript)

#Create more buttons
bt_next = tk.Button(window, text = "Next", command = getNext).grid(row=0, column=6, sticky = "WE")
bt_last = tk.Button(window, text = ">>",command = lambda: loadimage(maxnum)).grid(row=0, column=7, sticky = "WE")

#Create title
title_var = tk.StringVar(window)
title = tk.Label(window, textvariable = title_var).grid(row=1, columnspan=8)

#Create image panel
ph = Image.new("RGB", (512, 512))
image = ImageTk.PhotoImage(ph)
panel = tk.Label(window, image=image, width=800, bg="White")
panel.grid(row=2, column=0, columnspan=8, sticky="N")

#Create alt text and transcript
alt_var = tk.StringVar(window)
transcript_var = tk.StringVar(window)
alttext = tk.Label(window, textvariable = alt_var, wraplength = 600, height = 3).grid(row=4, columnspan=8)
transcriptlabel = tk.Label(window, textvariable=transcript_var, wraplength=600).grid(row=6, columnspan=8)

#Create separater between alt text and transcript
separator = tkinter.ttk.Separator(window, orient="horizontal").grid(row=5, column=0, columnspan=8, sticky='EW')

#Display first comic on startup
loadimage(currentnum)

#Update window
window.mainloop()