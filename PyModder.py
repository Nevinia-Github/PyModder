from tkinter import Tk, PhotoImage, VERTICAL, HORIZONTAL
from tkinter.ttk import Button, Separator
from Core.Utils.Config import Config
from Core.Utils.Project import Project
from Core.Widgets.Tooltip import ToolTip

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
            "Save": PhotoImage(file=os.path.join(self.paths["Images"], "save_icon.png")),
            "Launch": PhotoImage(file=os.path.join(self.paths["Images"], "launch_icon.png")),
            "Build": PhotoImage(file=os.path.join(self.paths["Images"], "build_icon.png"))
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
        launch_btn = Button(self.screen, image=self.icons["Launch"])
        build_btn = Button(self.screen, image=self.icons["Build"])

        separator_file_exe = Separator(self.screen, orient=VERTICAL)
        separator_exe_param = Separator(self.screen, orient=VERTICAL)
        separator_menu_other = Separator(self.screen, orient=HORIZONTAL)

        ToolTip(parameters_btn, "Paramètres")
        ToolTip(open_btn, "Ouvrir")
        ToolTip(save_btn, "Sauvegarder")
        ToolTip(new_btn, "Nouveau")
        ToolTip(launch_btn, "Lancer")
        ToolTip(build_btn, "Compiler")

        for i in range(8):
            if i in (3, 6):
                self.screen.columnconfigure(i, weight=1)
            else:
                self.screen.columnconfigure(i, weight=20)

        new_btn.grid(row=0, column=0, sticky="NSEW", padx=10, pady=5)
        open_btn.grid(row=0, column=1, sticky="NSEW", padx=10, pady=5)
        save_btn.grid(row=0, column=2, sticky="NSEW", padx=10, pady=5)
        separator_file_exe.grid(row=0, column=3, sticky="NS")
        launch_btn.grid(row=0, column=4, sticky="NSEW", padx=10, pady=5)
        build_btn.grid(row=0, column=5, sticky="NSEW", padx=10, pady=5)
        separator_exe_param.grid(row=0, column=6, sticky="NS")
        parameters_btn.grid(row=0, column=7, sticky="NSEW", padx=10, pady=5)
        separator_menu_other.grid(row=1, column=0, columnspan=8, sticky="EW")


PyModder()
