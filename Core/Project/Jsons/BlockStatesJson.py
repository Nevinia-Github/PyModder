import json
import os


class BlockStatesJson:
    def __init__(self, project, bloc):
        self.project = project
        self.bloc = bloc

    def save(self):
        os.makedirs(os.path.join(self.project.paths["Assets"], "blockstates"), exist_ok=True)
        file = {
            "variants": {
                "": {
                    "model": self.project.modid+":block/"+self.bloc.registry_name
                }
            }
        }
        with open(os.path.join(self.project.paths["Assets"], "blockstates", self.bloc.registry_name+".json"), "w") as f:
            f.write(json.dumps(file, indent=4))
