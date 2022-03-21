from tkinter import *

from interSection import InterSec, listInterSec


class MyFrame(Toplevel):

    def __init__(self, root, nbSecVertical, nbSecHorizontal):
        super().__init__(root)
        self.widthSec = 599
        self.heightSec = 246
        self.nb_Sec_Vert = nbSecVertical
        self.nb_Sec_Hor = nbSecHorizontal
        self.listSec = []
        self.geometry('1700x1080')

    def __exit__(self):
        try:
            for anySec in self.listSec:
                anySec.clearAllThread()
            else:
                self.destroy()
        except:
            for anySec in self.listSec:
                anySec.clearAllThread()
            return


    def lanceSimulaDE(self):
        try:
            index = 0
            for i in range(self.nb_Sec_Vert):
                for j in range(self.nb_Sec_Hor):
                    listInterSec.append(InterSec(self, (self.widthSec * j, self.heightSec * i), index=index))
                    index += 1
            self.listSec = listInterSec
        except:
            for anySec in self.listSec:
                anySec.clearAllThread()
            return


base = Tk()
WindowTitle = 'Tools for M2'
base.title(WindowTitle)
base.geometry("900x600")
base.resizable(width=FALSE, height=FALSE)
DE_Inter = MyFrame(base, 8, 2)

menu = Menu(base)
base.config(menu=menu)
filemenu1 = Menu(base)
menu.add_cascade(label="Settings", menu=filemenu1)
filemenu1.add_command(label="Start DE", command=DE_Inter.lanceSimulaDE)
filemenu1.add_command(label="Start AG", command=DE_Inter.__exit__)
filemenu1.add_separator()
filemenu1.add_command(label="Exit", command=base.quit)

base.mainloop()
