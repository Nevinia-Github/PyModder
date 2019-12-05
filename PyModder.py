from tkinter import Tk, HORIZONTAL, VERTICAL
from tkinter.ttk import Separator
from Core.Utils.Config import Config
from Core.Utils.Project import Project
from Core.Utils.Lang import Lang
from Core.Launcher.Launcher import Launcher
from Core.Widgets.MenuBar import MenuBar
from Core.Widgets.ElementsFrame import ElementsFrame
from Core.Widgets.PropertiesFrame import PropertiesFrame

import os


class PyModder:
    def __init__(self):
        self.version = (1, 0, 0)

        self.screen = Tk()

        self.paths = {
            "PyModder": os.path.dirname(__file__),
            "Mods": os.path.join(os.path.dirname(__file__), "Mods"),
            "Core": os.path.join(os.path.dirname(__file__), "Core"),
            "Images": os.path.join(os.path.dirname(__file__), "Core", "Images"),
            "Lang": os.path.join(os.path.dirname(__file__), "Core", "Lang")
        }

        self.conf = Config(os.path.join(self.paths["Core"], "config.json"))
        self.lang = Lang(os.path.join(self.paths["Lang"], self.conf.get("lang", "en")+".lang"))
        self.screen.state("zoomed")

        self.project = self.load_project(self.conf.get("last_project", ""))
        self.launcher = Launcher(self)
        self.conf.set("last_project", self.project.name)
        self.conf.save()

        self.screen.columnconfigure(1, weight=1)
        self.screen.columnconfigure(3, weight=3)
        self.screen.rowconfigure(3, weight=1)

        self.menu = MenuBar(self)
        self.elements = ElementsFrame(self)
        self.properties = PropertiesFrame(self)

        Separator(self.screen, orient=VERTICAL).grid(row=0, column=0, sticky="NS")
        Separator(self.screen, orient=HORIZONTAL).grid(row=0, column=0, columnspan=5, sticky="EW")
        self.menu.grid(row=1, column=1, columnspan=3, sticky="NESW")
        Separator(self.screen, orient=HORIZONTAL).grid(row=2, column=0, columnspan=5, sticky="EW")
        self.elements.grid(row=3, column=1, sticky="NESW")
        Separator(self.screen, orient=VERTICAL).grid(row=3, column=2, sticky="NS")
        self.properties.grid(row=3, column=3, sticky="NESW")
        Separator(self.screen, orient=VERTICAL).grid(row=0, column=4, sticky="NS")

        self.screen.mainloop()

    def load_project(self, name):
        if name == "":
            project = Project.new()
        else:
            project = Project(name)

        self.screen.title(project.name + " - PyModder")
        return project


PyModder()
