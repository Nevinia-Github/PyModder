import os
import json


class SimpleBlockJson:
    def __init__(self, project, bloc):
        self.project = project
        self.bloc = bloc

    def save(self):
        os.makedirs(os.path.join(self.project.paths["Assets"], "models", "block"), exist_ok=True)
        file = {
            "parent": "block/cube_all",
            "textures": {
                "all": self.project.modid+":block/"+self.bloc.texture
            }
        }
        with open(os.path.join(self.project.paths["Assets"], "models", "block", self.bloc.registry_name+".json"), "w") \
                as f:
            f.write(json.dumps(file, indent=4))


class BlockItemJson:
    def __init__(self, project, bloc):
        self.project = project
        self.bloc = bloc

    def save(self):
        os.makedirs(os.path.join(self.project.paths["Assets"], "models", "item"), exist_ok=True)
        file = {
            "parent": self.project.modid+":block/"+self.bloc.registry_name
        }
        with open(os.path.join(self.project.paths["Assets"], "models", "item", self.bloc.registry_name+".json"), "w") \
                as f:
            f.write(json.dumps(file, indent=4))
