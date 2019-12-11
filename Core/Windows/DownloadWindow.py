from tkinter import Toplevel
from tkinter.ttk import Label, Progressbar


class DownloadWindow(Toplevel):
    def __init__(self, main):
        super(DownloadWindow, self).__init__(main.screen)
        self.geometry("600x180+100+100")
        self.title(main.lang.get_translate("download_title", "Download"))

        Label(self, text=main.lang.get_translate("download_title", "Download"),
              font=("Arial", 15)).pack(padx=20, pady=20)
        self.current = Label(self, text=main.lang.get_translate("download_no", "No downloads available"),
                             font=("Arial", 12))
        self.current.pack(padx=20, pady=5)
        self.progress = Progressbar(self, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(padx=20, pady=20)
