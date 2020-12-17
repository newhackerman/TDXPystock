from tkinter import *

class App:
    def __init__(self,master):
        #self.frame=master
        frame1=Frame(root)
        frame2=Frame(root)
        frame1.pack(side=LEFT,padx=10,pady=10)
        frame2.pack(side=LEFT, padx=10, pady=10)

        button=Button(frame1,text='请勿乱动',fg='yellow',bg='black',command=self.say())
        button.pack()
        label = Label(frame1, text='请勿乱动',justify=LEFT,compound=CENTER,font=('宋体',35))
        label.pack()
        quit = Button(frame2, text="QUIT", command=root.destroy)
        quit.pack()
        root.update()
    @staticmethod
    def say():
        text = "This is Tcl/Tk version %s" % TclVersion
        text += "\nThis should be a cedilla: \xe7"
        print(text)

def say():
    text = "This is Tcl/Tk version %s" % TclVersion
    text += "\nThis should be a cedilla: \xe7"
    print(text)

root = Tk()

frame1=Frame(root)
frame2=Frame(root)
frame1.pack(side=LEFT,padx=10,pady=10)
frame2.pack(side=LEFT, padx=10, pady=10)

button=Button(frame1,text='请勿乱动',fg='yellow',bg='black',command=say)
button.pack()
label = Label(frame1, text='请勿乱动',justify=LEFT,compound=CENTER,font=('宋体',35))
label.pack()
quit = Button(frame2, text="QUIT", command=root.destroy)
quit.pack()

root.update()
root.mainloop()

#app=App(root)

# The following three commands are needed so the window pops
# up on top on Windows...
# root.iconify()
# root.update()
# root.deiconify()

