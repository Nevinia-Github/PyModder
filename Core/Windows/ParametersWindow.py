from tkinter.ttk import Button, Separator, Style
from tkinter import Toplevel, VERTICAL
from Core.Windows.ParametersPages.InformationsPage import InformationsPage
from Core.Windows.ParametersPages.GeneralPage import GeneralPage
from Core.Windows.ParametersPages.ProjectPage import ProjectPage


class ParametersWindow(Toplevel):
    def __init__(self, main):
        super(ParametersWindow, self).__init__(main.screen)
        self.main = main

        self.title(self.main.lang.get_translate("title_param", "Parameters"))
        self.geometry("800x600+{}+{}".format(int(self.winfo_screenwidth()/2 - 400),
                                             int(self.winfo_screenheight()/2 - 300)))

        self.columnconfigure(0, weight=1, minsize=100)
        self.columnconfigure(2, weight=1000)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        s = Style()
        s.configure('my.TButton', font=('Arial', 16))

        self.buttons = {
            "Informations": Button(self, text="Informations", style="my.TButton", command=lambda x=0: self.set_page(x)),
            "Général": Button(self, text="Général", style="my.TButton", command=lambda x=1: self.set_page(x)),
            "Projet": Button(self, text="Projet", style="my.TButton", command=lambda x=2: self.set_page(x))
        }

        self.pages = [
            InformationsPage(self),
            GeneralPage(self),
            ProjectPage(self)
        ]
        self.current_page = 0

        for k, v in enumerate(self.buttons.values()):
            v.grid(row=k, column=0, sticky="NESW", padx=10, pady=80)
        Separator(self, orient=VERTICAL).grid(row=0, column=1, rowspan=3, sticky="NS")
        self.pages[self.current_page].grid(row=0, column=2, rowspan=3, sticky="NEWS")

    def set_page(self, current_page):
        self.pages[self.current_page].grid_forget()
        self.current_page = current_page
        self.pages[self.current_page].grid(row=0, column=2, rowspan=3, sticky="NEWS")
