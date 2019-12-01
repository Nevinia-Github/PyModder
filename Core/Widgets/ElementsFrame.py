from tkinter.ttk import Frame, Separator, Label, Button, Style
from tkinter import HORIZONTAL


class ElementsFrame(Frame):
    def __init__(self, main):
        super(ElementsFrame, self).__init__(main.screen)

        s = Style()
        s.configure('my.TButton', font=('Arial', 16))

        self.main = main

        self.title = Label(self, text=main.lang.get_translate("elements_title", "Elements"), font=('Arial', '16'))
        add_element = Button(self, text=main.lang.get_translate("elements_add", "Add Element"), style="my.TButton")

        self.columnconfigure(0, weight=1)

        self.title.grid(row=0, column=0)
        Separator(self, orient=HORIZONTAL).grid(row=1, column=0, sticky="EW")
        add_element.grid(row=2, column=0, sticky="NESW")
