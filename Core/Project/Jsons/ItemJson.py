import os
import json


class SimpleItemJson:
    def __init__(self, project, item):
        self.project = project
        self.item = item

    def save(self):
        os.makedirs(os.path.join(self.project.paths["Assets"], "models", "item"), exist_ok=True)
        file = {
            "parent": "item/generated",
            "textures": {
                "all": self.project.modid+":item/"+self.item.texture
            }
        }
        with open(os.path.join(self.project.paths["Assets"], "models", "item", self.item.registry_name+".json"), "w") \
                as f:
            f.write(json.dumps(file, indent=4))
