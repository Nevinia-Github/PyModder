from tkinter.ttk import Frame, Separator, Label, Entry, Combobox, Button, Style
from tkinter import HORIZONTAL

from Core.Utils.Constants import BLOCK_MATERIALS


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
            else:
                other = Entry(self)
                other.grid(row=2+nb, column=1, sticky="EW", padx=50, pady=10)
                other.insert(0, v)
            nb += 1
            self.properties_widgets[k] = [label, other]

        s = Style()
        s.configure('test.TButton', font=('Arial', 14))

        btn = Button(self, text=self.main.lang.get_translate("properties_validate", "Validate"),
                     command=self.set_properties, style="test.TButton")
        btn.grid(row=2+nb, column=0, sticky="EW", padx=50, pady=20, columnspan=2)
        self.properties_widgets['BTN_VALIDATE'] = [btn]

    def set_properties(self):
        name = self.properties_widgets["name"][1].get()
        registry_name = self.properties_widgets["registry_name"][1].get().lower().replace(" ", "_")
        material = BLOCK_MATERIALS[self.properties_widgets["material"][1].current()]
        hardness = self.properties_widgets["hardness"][1].get()
        resistance = self.properties_widgets["resistance"][1].get()
        texture = self.properties_widgets["texture"][1].get()
        script = self.properties_widgets["script"][1].get()
        change = False

        if name != "" and name != self.current_obj.name:
            change = True
            old = self.current_obj.name
            self.current_obj.name = name
            self.main.elements.reload_object(old, self.current_obj)
        elif name == "":
            self.properties_widgets["name"][1].insert(0, self.current_obj.name)

        if registry_name != "" and registry_name != self.current_obj.registry_name:
            change = True
            self.current_obj.registry_name = registry_name
            self.properties_widgets["registry_name"][1].delete(0, "end")
            self.properties_widgets["registry_name"][1].insert(0, registry_name)
        elif registry_name == "":
            self.properties_widgets["registry_name"][1].insert(0, self.current_obj.registry_name)

        if material != self.current_obj.material:
            change = True
            self.current_obj.material = material

        if hardness != "" and hardness != self.current_obj.hardness:
            change = True
            self.current_obj.hardness = hardness
        elif hardness == "":
            self.properties_widgets["hardness"][1].insert(0, self.current_obj.hardness)

        if resistance != "" and resistance != self.current_obj.resistance:
            change = True
            self.current_obj.resistance = resistance
        elif resistance == "":
            self.properties_widgets["resistance"][1].insert(0, self.current_obj.resistance)

        if texture != "" and texture != self.current_obj.texture:
            change = True
            self.current_obj.texture = texture
        elif texture == "":
            self.properties_widgets["texture"][1].insert(0, self.current_obj.texture)

        if script != "" and script != self.current_obj.script:
            change = True
            self.current_obj.script = script
        elif script == "":
            self.properties_widgets["script"][1].insert(0, self.current_obj.script)

        if change:
            self.main.project.edit_objects()
