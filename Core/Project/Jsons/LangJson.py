import json
import os


class EnJson:
    def __init__(self, project):
        self.project = project

    def save(self):
        os.makedirs(os.path.join(self.project.paths["Assets"], "lang"), exist_ok=True)
        file = {}
        for i in self.project.objects["blocks"]:
            file["block."+self.project.modid+"."+i.registry_name] = i.name
        for i in self.project.objects["itemgroups"]:
            file["itemGroup."+i.registry_name] = i.name
        for i in self.project.objects["items"]:
            file["item."+self.project.modid+"."+i.registry_name] = i.name
        with open(os.path.join(self.project.paths["Assets"], "lang", "en_us.json"), "w") as f:
            f.write(json.dumps(file, indent=4))
