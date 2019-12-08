from tkinter.ttk import Frame, Separator, Label, Entry, Combobox, Button, Style, Checkbutton
from tkinter import HORIZONTAL, IntVar

from Core.Utils.Constants import BLOCK_MATERIALS, ITEMGROUP, ICON_BLOCKS


class PropertiesFrame(Frame):
    def __init__(self, main):
        super(PropertiesFrame, self).__init__(main.screen)
        self.main = main

        self.title = Label(self, text=main.lang.get_translate("properties_title", "Properties"), font=('Arial', '16'))

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=10)

        self.title.grid(row=0, column=0, columnspan=2)
        Separator(self, orient=HORIZONTAL).grid(row=1, column=0, columnspan=2, sticky="EW")

        self.properties_widgets = {}
        self.current_obj = None

    def show_properties(self, object_):
        for i in self.properties_widgets.values():
            for widget in i:
                if isinstance(widget, list):
                    widget[0].grid_forget()
                else:
                    widget.grid_forget()
        self.current_obj = object_
        nb = 0
        for k, v in object_.properties():
            label = Label(self, text=self.main.lang.get_translate("properties_"+k, k.replace("_", " ").title()+": "),
                          font=("Arial", "14"))
            label.grid(row=2+nb, column=0, sticky="EW", padx=10, pady=10)
            if k == "type_":
                other = Label(self, text=v, font=("Arial", "14"))
                other.grid(row=2+nb, column=1, sticky="EW", padx=50, pady=10)
            elif k == "material":
                other = Combobox(self, values=BLOCK_MATERIALS)
                other.current(BLOCK_MATERIALS.index(v))
                other.grid(row=2+nb, column=1, sticky="EW", padx=50, pady=10)
            elif k == "itemgroup":
                list_ = [i.name.upper().replace(" ", "_")+"_GROUP" for i in self.main.project.objects["itemgroups"]] + \
                        ITEMGROUP
                other = Combobox(self, values=list_)
                other.current(list_.index(v))
                other.grid(row=2+nb, column=1, sticky="EW", padx=50, pady=10)
            elif k == "icon":
                list_ = [i.name.upper().replace(" ", "_") for i in self.main.project.objects["blocks"]] + ICON_BLOCKS
                other = Combobox(self, values=list_)
                other.current(list_.index(v))
                other.grid(row=2+nb, column=1, sticky="EW", padx=50, pady=10)
            elif k == "search":
                var = IntVar()
                other = [Checkbutton(self, variable=var), var]
                if v:
                    other[0].invoke()
                other[0].grid(row=2+nb, column=1, sticky="EW", padx=50, pady=10)
            else:
                other = Entry(self)
                other.insert(0, v)
                other.grid(row=2+nb, column=1, sticky="EW", padx=50, pady=10)
            nb += 1
            self.properties_widgets[k] = [label, other]

        s = Style()
        s.configure('test.TButton', font=('Arial', 14))

        btn = Button(self, text=self.main.lang.get_translate("properties_validate", "Validate"),
                     command=self.set_properties, style="test.TButton")
        btn.grid(row=2+nb, column=0, sticky="EW", padx=50, pady=20, columnspan=2)
        self.properties_widgets['BTN_VALIDATE'] = [btn]

    def set_properties(self):
        change = self.current_obj.change(self.properties_widgets, self.main)
        if change:
            self.main.project.edit_objects()
