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
            "modid_label": Label(self, text=param.main.lang.get_translate("modid_project", "Mod ID : "),
                                font=("Arial", "14")),
            "modid_entry": Entry(self),
            "version_label": Label(self, text=param.main.lang.get_translate("version_project", "Version : "),
                                font=("Arial", "14")),
            "version_entry": Entry(self),
            "url_label": Label(self, text=param.main.lang.get_translate("url_project", "URL : "),
                                font=("Arial", "14")),
            "url_entry": Entry(self),
            "authors_label": Label(self, text=param.main.lang.get_translate("authors_project", "Authors : "),
                                font=("Arial", "14")),
            "authors_entry": Entry(self),
            "description_label": Label(self,
                                       text=param.main.lang.get_translate("description_project", "Description : "),
                                font=("Arial", "14")),
            "description_entry": Entry(self),

            "valide": Button(self, text=param.main.lang.get_translate("valide_project", "Validate"), style="my.TButton",
                             command=self.validate)
        }

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        self.widgets["name_entry"].insert(0, param.main.project.name)
        self.widgets["modid_entry"].insert(0, param.main.project.modid)
        self.widgets["version_entry"].insert(0, param.main.project.version)
        self.widgets["url_entry"].insert(0, param.main.project.url)
        self.widgets["authors_entry"].insert(0, param.main.project.authors)
        self.widgets["description_entry"].insert(0, param.main.project.description)

        for k, v in enumerate(self.widgets.values()):
            if k == 0:
                v.grid(row=k, column=0, sticky="NEWS", pady=20, padx=180, columnspan=2)
            elif k in (2, 4, 6, 8, 10, 12):
                v.grid(row=k-1, column=1, sticky="NESW", pady=10, padx=30)
            elif k == len(self.widgets.keys())-1:
                v.grid(row=k, column=0, sticky="NEWS", pady=20, padx=20, columnspan=2)
            else:
                v.grid(row=k, column=0, sticky="NEWS", pady=10, padx=30)

    def validate(self):
        name = self.widgets["name_entry"].get()
        modid = self.widgets["modid_entry"].get().lower()
        version = self.widgets["version_entry"].get()
        url = self.widgets["url_entry"].get()
        authors = self.widgets["authors_entry"].get()
        description = self.widgets["description_entry"].get()
        change = False

        if name != self.param.main.project.name:
            self.param.main.project.name = name
            change = True
        if modid != self.param.main.project.modid:
            self.param.main.project.modid = modid
            change = True
        if version != self.param.main.project.version:
            self.param.main.project.version = version
            change = True
        if url != self.param.main.project.url:
            self.param.main.project.url = url
            change = True
        if authors != self.param.main.project.authors:
            self.param.main.project.authors = authors
            change = True
        if description != self.param.main.project.description:
            self.param.main.project.description = description
            change = True

        if change:
            self.param.main.project.save()
            self.param.main.screen.title(name + " - PyModder")
            self.param.main.conf.set("last_project", name)
            self.param.main.conf.save()
