import os
import json


class Project:
    def __init__(self, name):
        self.path = os.path.join(os.path.dirname(__file__), "..", "..", "Mods", name)
        self.name = name

        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def save(self):
        print("Coming Soon")

    @classmethod
    def new(cls):
        name = "Untitled"
        while name in os.listdir(os.path.join(os.path.dirname(__file__), "..", "..", "Mods")):
            if name == "Untitled":
                name = name + "-1"
            else:
                name = name.split("-")[0] + "-" + str(int(name.split("-")[1])+1)
        return Project(name)