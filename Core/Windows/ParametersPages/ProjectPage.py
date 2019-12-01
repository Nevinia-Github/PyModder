from tkinter.ttk import Frame, Label


class ProjectPage(Frame):
    def __init__(self, param):
        super(ProjectPage, self).__init__(param)
        self.param = param

        self.labels = {
            "title": Label(self, text=param.main.lang.get_translate("title_projet", "Project Parameters"),
                           font=("Arial", "18"))
        }

        for k, v in enumerate(self.labels.values()):
            if k == 0:
                v.grid(row=k, column=0, sticky="NEWS", pady=20, padx=180)
            else:
                v.grid(row=k, column=0, sticky="NEWS", pady=10, padx=30)
