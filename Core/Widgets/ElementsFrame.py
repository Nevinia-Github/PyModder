from tkinter.ttk import Frame, Separator, Label, Button, Style
from tkinter import HORIZONTAL

from Core.Windows.AskElement import AskElement


class ElementsFrame(Frame):
    def __init__(self, main):
        super(ElementsFrame, self).__init__(main.screen)

        s = Style()
        s.configure('my.TButton', font=('Arial', 16))

        self.main = main
        self.ask = None  # RESPECT PEP8

        self.title = Label(self, text=main.lang.get_translate("elements_title", "Elements"), font=('Arial', '16'))
        add_element = Button(self, text=main.lang.get_translate("elements_add", "Add Element"), style="my.TButton",
                             command=self.add_elements)

        self.columnconfigure(0, weight=1)

        self.title.grid(row=0, column=0)
        Separator(self, orient=HORIZONTAL).grid(row=1, column=0, sticky="EW")
        add_element.grid(row=2, column=0, sticky="NESW", pady=5)
        Separator(self, orient=HORIZONTAL).grid(row=3, column=0, sticky="EW")

        self.current_row = 4

    def add_elements(self):
        self.ask = AskElement(self.main.screen, self.validate_add)

    def validate_add(self, name, type_):
        object_ = self.main.project.add_object(type_, name)
        Button(self, text=object_.name + " - " + object_.type_, style="my.TButton",
               command=lambda obj=object_: self.show_element(obj)).grid(row=self.current_row, column=0,
                                                                        sticky="EW", pady=5)
        self.current_row += 1

    def show_element(self, obj):
        self.main.properties.show_properties(obj)
