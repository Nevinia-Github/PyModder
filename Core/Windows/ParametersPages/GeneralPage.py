from tkinter.ttk import Frame, Label, Combobox, Button, Style
from tkinter.messagebox import showwarning


class GeneralPage(Frame):
    def __init__(self, param):
        super(GeneralPage, self).__init__(param)
        self.param = param

        s = Style()
        s.configure('my.TButton', font=('Arial', 16))

        self.widgets = {
            "title": Label(self, text=param.main.lang.get_translate("title_general", "General Parameters"),
                           font=("Arial", "18")),
            "lang_label": Label(self, text=param.main.lang.get_translate("lang_general", "Language : "),
                                font=("Arial", "14")),
            "lang_menu": Combobox(self, values=["English", "Français"]),

            "valide": Button(self, text=param.main.lang.get_translate("valide_general", "Validate"), style="my.TButton",
                             command=self.validate)
        }

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        if param.main.conf.get("lang", "en") == "en":
            self.widgets["lang_menu"].current(0)
        else:
            self.widgets["lang_menu"].current(1)

        for k, v in enumerate(self.widgets.values()):
            if k == 0:
                v.grid(row=k, column=0, sticky="NEWS", pady=20, padx=180, columnspan=2)
            elif k == 2:
                v.grid(row=k-1, column=1, sticky="NESW", pady=10, padx=30)
            elif k == len(self.widgets.keys())-1:
                v.grid(row=k, column=0, sticky="NEWS", pady=20, padx=20, columnspan=2)
            else:
                v.grid(row=k, column=0, sticky="NEWS", pady=10, padx=30)

    def validate(self):
        lang = ["en", "fr"][self.widgets["lang_menu"].current()]
        change = False
        if lang != self.param.main.conf.get("lang", "en"):
            self.param.main.conf.set("lang", lang)
            change = True

        if change:
            self.param.main.conf.save()
            showwarning("Changement Validé", "Veuillez redémarrer pour prendre en compte les changements.")

