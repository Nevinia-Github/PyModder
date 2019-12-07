from tkinter.ttk import Frame, Separator, Label, Entry
from tkinter import HORIZONTAL


class PropertiesFrame(Frame):
    def __init__(self, main):
        super(PropertiesFrame, self).__init__(main.screen)
        self.main = main

        self.title = Label(self, text=main.lang.get_translate("properties_title", "Properties"), font=('Arial', '16'))

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=10)

        self.title.grid(row=0, column=0, columnspan=2)
        Separator(self, orient=HORIZONTAL).grid(row=1, column=0, columnspan=2, sticky="EW")

        self.properties_widgets = []

    def show_properties(self, object_):
        for i in self.properties_widgets:
            for widget in i:
                widget.grid_forget()
        nb = 0
        for k, v in object_.properties():
            label = Label(self, text=self.main.lang.get_translate("properties_"+k, k.replace("_", " ").title()+": "),
                          font=("Arial", "14"))
            label.grid(row=2+nb, column=0, sticky="EW", padx=10, pady=10)
            if k == "type_":
                label = Label(self, text=v, font=("Arial", "14"))
                label.grid(row=2+nb, column=1, sticky="EW", padx=50, pady=10)
            else:
                entry = Entry(self)
                entry.grid(row=2+nb, column=1, sticky="EW", padx=50, pady=10)
                entry.insert(0, v)
            nb += 1
            self.properties_widgets.append([label, entry])
