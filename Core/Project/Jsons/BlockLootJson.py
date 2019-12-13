import os
import json


class SimpleBlockLootJson:
    def __init__(self, project, block):
        self.project = project
        self.block = block

    def save(self):
        os.makedirs(os.path.join(self.project.paths["Ressources"], "data", self.project.modid, "loot_tables", "blocks"),
                    exist_ok=True)
        file = {
            "type": "minecraft:block",
            "pools": [
                {
                    "name": self.block.registry_name,
                    "rolls": 1,
                    "entries": [
                        {
                            "type": "minecraft:item",
                            "name": self.project.modid + ":" + self.block.registry_name
                        }
                    ]
                }
            ]
        }
        with open(os.path.join(self.project.paths["Ressources"], "data", self.project.modid, "loot_tables", "blocks",
                               self.block.registry_name+".json"), "w") as f:
            f.write(json.dumps(file, indent=4))
