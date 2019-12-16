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

        self.elements_widgets = {}

        self.current_row = 4

    def add_elements(self):
        self.ask = AskElement(self.main.screen, self.validate_add)

    def validate_add(self, name, type_):
        print(name)
        object_ = self.main.project.add_object(type_, name)
        self.add_object(object_)

    def reload_object(self, name, obj):
        if name in self.elements_widgets.keys():
            btn = self.elements_widgets[name]
            del self.elements_widgets[name]
            btn.config(text=obj.name + " - " + obj.type_)
            self.elements_widgets[obj.name] = btn

    def add_object(self, obj):
        btn = Button(self, text=obj.name + " - " + obj.type_, style="my.TButton",
                     command=lambda obj_=obj: self.show_element(obj_))
        btn.grid(row=self.current_row, column=0, sticky="EW", pady=5)
        self.elements_widgets[obj.name] = btn
        self.current_row += 1

    def show_element(self, obj):
        self.main.properties.show_properties(obj)
