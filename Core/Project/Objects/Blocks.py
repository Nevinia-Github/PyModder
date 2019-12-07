class SimpleBlock:
    def __init__(self, name="Block", texture="", material="ROCK", hardness="25F", resistance="600F",
                 registry_name=None, script=""):
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
        self.type_ = "SimpleBlock"

    def properties(self):
        return self.__dict__.items()

    def to_json(self):
        return {"name": self.name, "registry_name": self.registry_name, "material": self.material,
                "hardness": self.hardness, "resistance": self.resistance, "texture": self.texture, "type": self.type_,
                "script": self.script}

    @classmethod
    def from_json(cls, datas):
        name = datas["name"]
        registry_name = datas["registry_name"]
        material = datas["material"]
        hardness = datas["hardness"]
        resistance = datas["resistance"]
        texture = datas["texture"]
        script = datas["script"]
        return SimpleBlock(name, texture, material, hardness, resistance, registry_name, script)

    def __str__(self):
        return "Block({}, {}, {}, {}, {}, {})".format(self.name, self.texture, self.registry_name, self.material,
                                                      self.hardness, self.resistance)
