from tkinter import Label


class Car(Label):
    def __init__(self,root, index, img):
        super().__init__(root)
        self.config(image=img)
        self.index = index