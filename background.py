import customtkinter as ctk
from tkinter import Frame
from PIL import Image


class BackgroundLabel(ctk.CTkLabel):
    def __init__(self, master):
        super().__init__(master)
        self.image = ctk.CTkImage(dark_image=Image.open('images/circuitboard.jpeg'),
                                  size=(850, 850))
        self.configure(text="", image=self.image, anchor='center')
        self.pack(expand=1, fill='both')


class BackgroundFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.background = BackgroundLabel(self)
        self.pack()
