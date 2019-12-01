from tkinter.ttk import Frame, Label
from tkinter import TkVersion, TclVersion
from sys import version_info


class InformationsPage(Frame):
    def __init__(self, param):
        super(InformationsPage, self).__init__(param)
        self.param = param

        version_python = ".".join(str(i) for i in version_info[:3])
        version = ".".join(str(i) for i in version_info[:3])

        self.widgets = {
            "title": Label(self, text=param.main.lang.get_translate("title_informations", "PyModder"),
                           font=("Arial", "18")),
            "create": Label(self, text=param.main.lang.get_translate("create_informations", "Create by Nevinia"),
                            font=("Arial", "14")),
            "version": Label(self, text=param.main.lang.get_translate("version_infomations", "Version : {}",
                                                                      version), font=("Arial", "14")),
            "pyver": Label(self, text=param.main.lang.get_translate("pyver_informations", "Version Python : {}",
                                                                    version_python), font=("Arial", "14")),
            "tkver": Label(self, text=param.main.lang.get_translate("tkver_informations", "Version Tkinter : {}",
                                                                    TkVersion), font=("Arial", "14")),
            "tclver": Label(self, text=param.main.lang.get_translate("tclver_informations", "Version Tcl : {}",
                                                                     TclVersion), font=("Arial", "14"))
        }

        for k, v in enumerate(self.widgets.values()):
            if k == 0:
                v.grid(row=k, column=0, sticky="NEWS", pady=20, padx=250)
            else:
                v.grid(row=k, column=0, sticky="NEWS", pady=10, padx=30)
