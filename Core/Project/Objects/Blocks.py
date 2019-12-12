from Core.Utils.Constants import BLOCK_MATERIALS, ITEMGROUP


class SimpleBlock:
    def __init__(self, name="Block", texture="", material="ROCK", hardness="25F", resistance="600F",
                 registry_name=None, script="", itemgroup="BUILDING_BLOCKS"):
        self.name = name
        if registry_name is None:
            self.registry_name = name.lower().replace(" ", "_")
        else:
            self.registry_name = registry_name.lower().replace(" ", "_")
        self.material = material
        self.hardness = hardness
        self.resistance = resistance
        self.texture = texture
        self.script = script
        self.itemgroup = itemgroup
        self.type_ = "SimpleBlock"

    def change(self, properties_widgets, main):
        name = properties_widgets["name"][1].get()
        registry_name = properties_widgets["registry_name"][1].get().lower().replace(" ", "_")
        material = BLOCK_MATERIALS[properties_widgets["material"][1].current()]
        list_ = [i.name.upper().replace(" ", "_") + "_GROUP" for i in main.project.objects["itemgroups"]] + ITEMGROUP
        itemgroup = list_[properties_widgets["itemgroup"][1].current()]
        hardness = properties_widgets["hardness"][1].get()
        resistance = properties_widgets["resistance"][1].get()
        texture = properties_widgets["texture"][1].get()
        script = properties_widgets["script"][1].get("1.0")
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

        if material != self.material:
            change = True
            self.material = material

        if itemgroup != self.itemgroup:
            change = True
            self.itemgroup = itemgroup

        if hardness != "" and hardness != self.hardness:
            change = True
            self.hardness = hardness
        elif hardness == "":
            properties_widgets["hardness"][1].insert(0, self.hardness)

        if resistance != "" and resistance != self.resistance:
            change = True
            self.resistance = resistance
        elif resistance == "":
            properties_widgets["resistance"][1].insert(0, self.resistance)

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
        return {"name": self.name, "registry_name": self.registry_name, "material": self.material,
                "hardness": self.hardness, "resistance": self.resistance, "texture": self.texture,
                "itemgroup": self.itemgroup, "type": self.type_, "script": self.script}

    @classmethod
    def from_json(cls, datas):
        name = datas["name"]
        registry_name = datas["registry_name"]
        material = datas["material"]
        hardness = datas["hardness"]
        resistance = datas["resistance"]
        texture = datas["texture"]
        itemgroup = datas["itemgroup"]
        script = datas["script"]
        return SimpleBlock(name, texture, material, hardness, resistance, registry_name, script, itemgroup)

    def __str__(self):
        return "{}({}, {}, {}, {}, {}, {}, {})".format(self.type_, self.name, self.texture, self.registry_name,
                                                       self.material, self.hardness, self.resistance, self.itemgroup)
