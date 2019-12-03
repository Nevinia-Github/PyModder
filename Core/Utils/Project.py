import os
import json


class Project:
    def __init__(self, name):
        self.path = os.path.join(os.path.dirname(__file__), "..", "..", "Mods", name)
        self.name = name
        self.old_name = name

        if not os.path.exists(self.path):
            os.makedirs(self.path)
            with open(os.path.join(self.path, "project.json"), "w") as f:
                json.dump({"name": name}, f, indent=4)

    def save(self):
        with open(os.path.join(self.path, "project.json"), "w") as f:
            json.dump({"name": self.name}, f, indent=4)

        if self.old_name != self.name:
            path = os.path.join(os.path.dirname(__file__), "..", "..", "Mods", self.name)
            os.rename(self.path, path)
            self.path = path
            self.old_name = self.name

    @classmethod
    def new(cls):
        name = "Untitled"
        while name in os.listdir(os.path.join(os.path.dirname(__file__), "..", "..", "Mods")):
            if name == "Untitled":
                name = name + "-1"
            else:
                name = name.split("-")[0] + "-" + str(int(name.split("-")[1])+1)
        return Project(name)