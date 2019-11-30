from tkinter import Tk, PhotoImage, Button
from Core.Utils.Config import Config
from Core.Utils.Project import Project

import os


class PyModder:
    def __init__(self):
        self.screen = Tk()

        self.paths = {
            "PyModder": os.path.dirname(__file__),
            "Mods": os.path.join(os.path.dirname(__file__), "Mods"),
            "Core": os.path.join(os.path.dirname(__file__), "Core"),
            "Images": os.path.join(os.path.dirname(__file__), "Core", "Images")
        }
        self.icons = {
            "Parameters": PhotoImage(file=os.path.join(self.paths["Images"], "parameters_icon.png")),
            "Open": PhotoImage(file=os.path.join(self.paths["Images"], "open_icon.png")),
            "New": PhotoImage(file=os.path.join(self.paths["Images"], "new_icon.png")),
            "Save": PhotoImage(file=os.path.join(self.paths["Images"], "save_icon.png"))
        }

        self.conf = Config(os.path.join(self.paths["Core"], "config.json"))
        self.screen.state("zoomed")

        self.project = self.load_project(self.conf.get("last_project", ""))

        self.setup_ui()

        self.screen.mainloop()

    def load_project(self, name):
        if name == "":
            project = Project.new()
        else:
            project = Project(name)

        self.screen.title(project.name + " - PyModder")
        return project

    def setup_ui(self):

        parameters_btn = Button(self.screen, image=self.icons["Parameters"])
        open_btn = Button(self.screen, image=self.icons["Open"])
        save_btn = Button(self.screen, image=self.icons["Save"])
        new_btn = Button(self.screen, image=self.icons["New"])
        new_btn.grid(row=0, column=0)
        open_btn.grid(row=0, column=1)
        save_btn.grid(row=0, column=2)
        parameters_btn.grid(row=0, column=4)


PyModder()
