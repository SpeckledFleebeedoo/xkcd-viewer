import tkinter as tk
from urllib.request import urlopen
import json
import random
import webbrowser
import tkinter.ttk
from PIL import ImageTk, Image
from io import BytesIO

#Get number of latest comic
info = json.loads(urlopen("https://xkcd.com/info.0.json").read())
currentnum = maxnum = info["num"]

#Scroll canvas when using mouse wheel
def mouse_scroll(event, canvas):
    if event.delta:
        canvas.yview_scroll(int(-1*(event.delta/120)), 'units')
    else:
        if event.num == 5:
            move = 1
        else:
            move = -1

        canvas.yview_scroll(move, 'units')

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

#Show comic transcript
def showTranscript():
    global info
    separator.grid(row=5, column=0, columnspan=9, sticky='EW')
    transcriptlabel.grid(row=6, columnspan=8)
    transcript = info["transcript"]
    if transcript == "":
        transcript = "No transcript available"
    try:
        transcript_var.set(transcript)
    except:
        transcript_var.set("Cannot show transcript")

#Load and display comic
def loadimage(comicnum):

    #Update current comic numbervv
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
    transcriptlabel.grid_remove()
    separator.grid_remove()
    
    #Download image
    img_url = info["img"]
    img_data = urlopen(img_url).read()
    image = Image.open(BytesIO(img_data))

    #Display image
    image = ImageTk.PhotoImage(image)
    canvas.create_image((400-image.width()/2), 2, image=image, anchor="nw")
    canvas.create_line((0,0),(0,10), fill="SystemButtonFace")
    canvas.configure(scrollregion=canvas.bbox("all"))
    canvas.image=image

root = tk.Tk()
root.title("xkcd")

#BUTTONS_________________________________________________________________________________________________________
bt_first = tk.Button(root, text = "<<",command = lambda: loadimage(1)).grid(row=0, column=0, sticky = "WE")
bt_prev = tk.Button(root, text = "Previous", command = getPrev).grid(row=0, column=1, sticky = "WE")
bt_random = tk.Button(root, text = "Random", command = getRandom).grid(row=0, column=2, sticky = "WE")

int_box = tk.Entry(root)
int_box.grid(row=0, column=3, sticky="WE", padx=2)
int_box.insert(0, str(currentnum))
int_box.bind('<Return>', goToNum)
int_box.bind("<FocusIn>", lambda args: int_box.delete('0', 'end'))
bt_goto = tk.Button(root, text = "Go", command = goToNum).grid(row=0, column=4, sticky="WE")

menubutton = tk.Menubutton(root, text = "Options", relief="raised", bd=2)
menubutton.grid(row=0, column=5, sticky = "NESW")
menubutton.menu = tk.Menu(menubutton)
menubutton["menu"]=menubutton.menu
menubutton.menu.add_command(label = "Explain", command = lambda: webbrowser.open(f"www.explainxkcd.com/{currentnum}"))
menubutton.menu.add_command(label = "Original", command = lambda: webbrowser.open(f"www.xkcd.com/{currentnum}"))
menubutton.menu.add_command(label = "Transcript", command = showTranscript)

bt_next = tk.Button(root, text = "Next", command = getNext).grid(row=0, column=6, sticky = "WE")
bt_last = tk.Button(root, text = ">>",command = lambda: loadimage(maxnum)).grid(row=0, column=7, sticky = "WE")

#TITLE__________________________________________________________________________________________________________________
title_var = tk.StringVar(root)
title = tk.Label(root, textvariable = title_var, height = 2).grid(row=1, columnspan=8)

#COMIC__________________________________________________________________________________________________________________
canvas = tk.Canvas(root, width = 800, height = 600)
canvas.grid(row=2, column=0, columnspan=8)

root.bind_all('<MouseWheel>', lambda event, canvas=canvas: mouse_scroll(event, canvas))

scroll_y = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scroll_y.grid(row=0, column=8, rowspan=6, sticky="ns")

canvas.configure(yscrollcommand=scroll_y.set)
canvas.configure(scrollregion=canvas.bbox("all"))

#ALT TEXT______________________________________________________________________________________________________________
alt_var = tk.StringVar(root)
alttext = tk.Label(root, textvariable = alt_var, wraplength = 700, height = 3).grid(row=4, columnspan=8)

#TRANSCRIPT____________________________________________________________________________________________________________
separator = tkinter.ttk.Separator(root, orient="horizontal")
transcript_var = tk.StringVar(root)
transcriptlabel = tk.Label(root, textvariable=transcript_var, wraplength=800)

loadimage(currentnum)       #Display first comic on startup
root.mainloop()             #Start mainloop