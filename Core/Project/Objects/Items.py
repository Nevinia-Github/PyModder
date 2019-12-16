from Core.Utils.Constants import ITEMGROUP


class SimpleItem:
    def __init__(self, name="Item", texture="", registry_name=None, script="", itemgroup="MATERIALS", stacksize=64):
        self.name = name
        if registry_name is None:
            self.registry_name = name.lower().replace(" ", "_")
        else:
            self.registry_name = registry_name.lower().replace(" ", "_")
        self.texture = texture
        self.itemgroup = itemgroup
        self.stacksize = stacksize
        self.script = script
        self.type_ = "SimpleItem"

    def change(self, properties_widgets, main):
        name = properties_widgets["name"][1].get()
        registry_name = properties_widgets["registry_name"][1].get().lower().replace(" ", "_")
        list_ = [i.name.upper().replace(" ", "_") + "_GROUP" for i in main.project.objects["itemgroups"]] + ITEMGROUP
        itemgroup = list_[properties_widgets["itemgroup"][1].current()]
        texture = properties_widgets["texture"][1].get()
        stacksize = properties_widgets["stacksize"][1].get()
        script = properties_widgets["script"][1].get("1.0", "end")
        change = False

        if name != "" and name != self.name:
            change = True
            old = self.name
            self.name = name
            main.elements.reload_object(old, self)
        elif name == "":
            properties_widgets["name"][1].insert(0, self.name)

        if registry_name != "" and registry_name != self.registry_name:
            change = True
            self.registry_name = registry_name
            properties_widgets["registry_name"][1].delete(0, "end")
            properties_widgets["registry_name"][1].insert(0, registry_name)
        elif registry_name == "":
            properties_widgets["registry_name"][1].insert(0, self.registry_name)

        if stacksize != "" and stacksize != self.stacksize:
            change = True
            self.stacksize = stacksize
        elif stacksize == "":
            properties_widgets["stacksize"][1].insert(0, self.stacksize)

        if itemgroup != self.itemgroup:
            change = True
            self.itemgroup = itemgroup

        if texture != "" and texture != self.texture:
            change = True
            self.texture = texture
        elif texture == "":
            properties_widgets["texture"][1].insert(0, self.texture)

        if script != "" and script != self.script:
            change = True
            self.script = script
        elif script == "":
            properties_widgets["script"][1].insert("1.0", self.script)

        return change

    def properties(self):
        return self.__dict__.items()

    def to_json(self):
        return {"name": self.name, "registry_name": self.registry_name, "texture": self.texture,
                "itemgroup": self.itemgroup, "stacksize": self.stacksize, "type": self.type_, "script": self.script}

    @classmethod
    def from_json(cls, datas):
        name = datas["name"]
        registry_name = datas["registry_name"]
        texture = datas["texture"]
        itemgroup = datas["itemgroup"]
        script = datas["script"]
        stacksize = datas["stacksize"]
        return SimpleItem(name, texture, registry_name, script, itemgroup, stacksize)

    def __str__(self):
        return "{}({}, {}, {}, {}, {})".format(self.type_, self.name, self.texture, self.registry_name, self.itemgroup,
                                               self.stacksize)
