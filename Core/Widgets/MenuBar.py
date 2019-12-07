from tkinter.ttk import Frame, Button, Separator
from tkinter import PhotoImage, VERTICAL
from tkinter.messagebox import showinfo, showerror
from Core.Widgets.Tooltip import ToolTip
from Core.Windows.ParametersWindow import ParametersWindow
from Core.Launcher.Launcher import Launcher

import os
import subprocess
import shutil


class MenuBar(Frame):
    def __init__(self, main):
        super(MenuBar, self).__init__(main.screen)
        self.main = main

        self.icons = {
            "Parameters": PhotoImage(file=os.path.join(main.paths["Images"], "parameters_icon.png")),
            "Open": PhotoImage(file=os.path.join(main.paths["Images"], "open_icon.png")),
            "New": PhotoImage(file=os.path.join(main.paths["Images"], "new_icon.png")),
            "Save": PhotoImage(file=os.path.join(main.paths["Images"], "save_icon.png")),
            "Launch": PhotoImage(file=os.path.join(main.paths["Images"], "launch_icon.png")),
            "Build": PhotoImage(file=os.path.join(main.paths["Images"], "build_icon.png"))
        }

        self.param_btn = Button(self, image=self.icons["Parameters"], command=self.open_param)
        self.open_btn = Button(self, image=self.icons["Open"])
        self.save_btn = Button(self, image=self.icons["Save"])
        self.new_btn = Button(self, image=self.icons["New"], command=self.new)
        self.launch_btn = Button(self, image=self.icons["Launch"], command=self.launch)
        self.build_btn = Button(self, image=self.icons["Build"], command=self.build)

        ToolTip(self.param_btn, main.lang.get_translate("parameters_tooltip", "Parameters"))
        ToolTip(self.open_btn, main.lang.get_translate("open_tooltip", "Open"))
        ToolTip(self.save_btn, main.lang.get_translate("save_tooltip", "Save"))
        ToolTip(self.new_btn, main.lang.get_translate("new_tooltip", "New"))
        ToolTip(self.launch_btn, main.lang.get_translate("launch_tooltip", "Launch"))
        ToolTip(self.build_btn, main.lang.get_translate("build_tooltip", "Build"))

        self.separators = {
            "file_exe": Separator(self, orient=VERTICAL),
            "exe_param": Separator(self, orient=VERTICAL),
            "left": Separator(self, orient=VERTICAL),
            "right": Separator(self, orient=VERTICAL)
        }

        for i in range(8):
            if i in (3, 6):
                self.columnconfigure(i, weight=0)
            else:
                self.columnconfigure(i, weight=1)

        self.new_btn.grid(row=0, column=0, sticky="NSEW", padx=5, pady=5)
        self.open_btn.grid(row=0, column=1, sticky="NSEW", padx=5, pady=5)
        self.save_btn.grid(row=0, column=2, sticky="NSEW", padx=5, pady=5)
        self.separators["file_exe"].grid(row=0, column=3, sticky="NS")
        self.launch_btn.grid(row=0, column=4, sticky="NSEW", padx=5, pady=5)
        self.build_btn.grid(row=0, column=5, sticky="NSEW", padx=5, pady=5)
        self.separators["exe_param"].grid(row=0, column=6, sticky="NS")
        self.param_btn.grid(row=0, column=7, sticky="NSEW", padx=5, pady=5)

    def new(self):
        self.main.project = self.main.load_project("")
        self.main.launcher = Launcher(self.main)
        self.main.conf.set("last_project", self.main.project.name)
        self.main.conf.save()

    def launch(self):
        self.main.launcher.launch()

    def build(self):
        showinfo("Compilation à venir", "La compilation va être effectuée.\nElle peut prendre quelques minutes et "
                                        "l'application peut être gelée. Attendez le temps de la compilation.\n"
                                        "Appuyez sur 'Ok' pour continuer.")
        sub = subprocess.run(["cd", self.main.project.paths["Folder"], "&&", r".\gradlew.bat", "build"],
                             capture_output=True, shell=True)
        path = os.path.join(self.main.project.paths["Folder"], "build", "libs",
                            self.main.project.name + "-" + self.main.project.version + ".jar")
        shutil.copy(path, os.path.join(self.main.project.paths["Folder"],
                                       self.main.project.name + "-" + self.main.project.version + ".jar"))
        if sub.stderr != '':
            showinfo("Compilation finie",
                     "Compilation finie.\nVotre fichier est disponible dans le dossier du mods.\nSon nom est " +
                     self.main.project.name + "-" + self.main.project.version + ".jar")
        else:
            showerror("Compilation finie", "La compilation a échoué.\nErreur : "+sub.stderr)

    def open_param(self):
        ParametersWindow(self.main)
