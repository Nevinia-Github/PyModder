from Core.Utils.Constants import ICON_BLOCKS


class ItemGroup:
    def __init__(self, name="Group", registry_name=None, icon="Blocks.DIRT", search=False, script=""):
        self.name = name
        if registry_name is None:
            self.registry_name = name.lower().replace(" ", "_")
        else:
            self.registry_name = registry_name.lower().replace(" ", "_")
        self.icon = icon
        self.search = search
        self.script = script
        self.type_ = "ItemGroup"

    def change(self, properties_widgets, main):
        name = properties_widgets["name"][1].get()
        registry_name = properties_widgets["registry_name"][1].get().lower().replace(" ", "_")
        list_ = [i.name.upper().replace(" ", "_") for i in main.project.objects["blocks"]] + ICON_BLOCKS
        icon = list_[properties_widgets["icon"][1].current()]
        search = properties_widgets["search"][1][1].get()
        if search == 1:
            search = True
        else:
            search = False
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

        if icon != self.icon:
            change = True
            self.icon = icon

        if search != self.search:
            change = True
            self.search = search

        if script != "" and script != self.script:
            change = True
            self.script = script
        elif script == "":
            properties_widgets["script"][1].insert(0, self.script)

        return change

    def properties(self):
        return self.__dict__.items()

    def to_json(self):
        return {"name": self.name, "registry_name": self.registry_name, "icon": self.icon, "search": self.search,
                "type": self.type_, "script": self.script}

    @classmethod
    def from_json(cls, datas):
        name = datas["name"]
        registry_name = datas["registry_name"]
        icon = datas["icon"]
        search = datas["search"]
        script = datas["script"]
        return ItemGroup(name, registry_name, icon, search, script)

    def __str__(self):
        return "{}({}, {}, {}, {})".format(self.type_, self.name, self.registry_name, self.icon, self.search)
