from tkinter import Toplevel
from tkinter.ttk import Label, Entry, Button, Combobox

from Core.Utils.Constants import ELEMENTS


class AskElement(Toplevel):
    def __init__(self, window, callback):
        super(AskElement, self).__init__(window)
        self.window = window
        self.callback = callback

        self.clabel = Label(self, text="Entrez le type de l'élément :", font=("Arial", "14"))
        self.combo = Combobox(self, values=ELEMENTS)
        self.elabel = Label(self, text="Entrez le nom de l'élément :", font=("Arial", "14"))
        self.entry = Entry(self)
        self.button = Button(self, text="Valider", command=self.valide)

        self.combo.current(0)

        self.clabel.pack(padx=10, pady=10)
        self.combo.pack(padx=10, pady=7)
        self.elabel.pack(padx=10, pady=17)
        self.entry.pack(padx=10, pady=0)
        self.button.pack(padx=10, pady=7)

        self.title("Ajouter Element")

    def valide(self):
        name = self.entry.get()
        type_ = ELEMENTS[self.combo.current()]
        if name != "":
            self.callback(name, type_)
            self.destroy()
