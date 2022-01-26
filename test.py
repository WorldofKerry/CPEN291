from tkinter import *

window = Tk()

variable = 0

def jeez(): 
    global variable
    variable = variable + 1

button1 = Button(window, text = "OK", command = jeez)
button1.pack()

label = Label(window, text = "Welcome to Python")
label.pack()

entryName = Entry(window, text=str(variable))
entryName.pack()

window.mainloop()