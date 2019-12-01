from tkinter.ttk import Frame, Separator, Label
from tkinter import HORIZONTAL


class PropertiesFrame(Frame):
    def __init__(self, main):
        super(PropertiesFrame, self).__init__(main.screen)
        self.main = main

        self.title = Label(self, text=main.lang.get_translate("properties_title", "Properties"), font=('Arial', '16'))

        self.columnconfigure(0, weight=1)

        self.title.grid(row=0, column=0)
        Separator(self, orient=HORIZONTAL).grid(row=1, column=0, sticky="EW")
