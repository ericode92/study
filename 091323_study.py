from tkinter import *

food = ["Pizza", "KFC", "Coke"]

def order():
    if(x.get() == 0):
        print("You picked a Pizza.")
    elif(x.get() == 1):
        print("You picked KFC.")
    elif(x.get() == 2):
        print("You picked Cocacola.")
    else:
        print("Sorry?")


window = Tk()
window.title("Let's eat 여보!")

x = IntVar()

for index in range(len(food)):
    radiobutton = Radiobutton(window,
                              text=food[index],
                              variable=x,
                              value=index,
                              padx=25,
                              font=("Impact", 25),
                              compound=LEFT, # how will it change?
                              indicatoron=0,
                              width=700,
                              command=order)
    
    radiobutton.pack()

window.mainloop()