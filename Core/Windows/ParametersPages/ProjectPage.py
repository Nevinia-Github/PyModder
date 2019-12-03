from tkinter.ttk import Frame, Label, Button, Entry, Style
from tkinter.messagebox import showwarning


class ProjectPage(Frame):
    def __init__(self, param):
        super(ProjectPage, self).__init__(param)
        self.param = param

        s = Style()
        s.configure('my.TButton', font=('Arial', 16))

        self.widgets = {
            "title": Label(self, text=param.main.lang.get_translate("title_project", "Project Parameters"),
                           font=("Arial", "18")),
            "name_label": Label(self, text=param.main.lang.get_translate("name_project", "Name : "),
                                font=("Arial", "14")),
            "name_entry": Entry(self),

            "valide": Button(self, text=param.main.lang.get_translate("valide_project", "Validate"), style="my.TButton",
                             command=self.validate)
        }

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        self.widgets["name_entry"].insert(0, param.main.project.name)

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
        name = self.widgets["name_entry"].get()
        change = False
        if name != self.param.main.project.name:
            self.param.main.project.name = name
            change = True

        if change:
            self.param.main.project.save()
            self.param.main.screen.title(name + " - PyModder")
