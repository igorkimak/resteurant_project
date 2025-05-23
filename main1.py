import tkinter as tk
from tkinter import simpledialog, messagebox
from klasy import Danie, DanieWeganskie, Menu, Stolik, Kelner, DanieDialog, StolikDialog, KelnerDialog
import gc

class Aplikacja:
    def __init__(self, root):
        self.root = root
        self.root.title("Restauracja")

        self.menu = Menu()
        self.stoliki = []
        self.kelnerzy = []

        self.dodaj_domyslne_dania()
        self.setup()

    def dodaj_domyslne_dania(self):
        domyslne_dania = [
            Danie("Spaghetti", 25.0),
            Danie("Pizza Margherita", 20.0),
            Danie("Sałatka Cezar", 18.0),
            DanieWeganskie("Zupa Pomidorowa", 12.0, ["pomidory", "wegańska śmietana"]),
            Danie("Burger Wołowy", 22.0)
        ]
        for danie in domyslne_dania:
            self.menu.dodaj_danie(danie)

    def setup(self):
        # stoliki
        self.stoliki_frame = tk.LabelFrame(self.root, text="Stoliki")
        self.stoliki_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.stoliki_listbox = tk.Frame(self.stoliki_frame)
        self.stoliki_listbox.pack(fill=tk.BOTH, expand=True)

        self.stoliki_add = tk.Button(self.stoliki_frame, text="Dodaj stolik", command=self.dodaj_stolik)
        self.stoliki_add.pack()

        # kelnerzy
        self.kelnerzy_frame = tk.LabelFrame(self.root, text="Kelnerzy")
        self.kelnerzy_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.kelnerzy_listbox = tk.Frame(self.kelnerzy_frame)
        self.kelnerzy_listbox.pack(fill=tk.BOTH, expand=True)

        self.kelnerzy_add = tk.Button(self.kelnerzy_frame, text="Dodaj kelnera", command=self.dodaj_kelnera)
        self.kelnerzy_add.pack()

        self.menu_frame = tk.LabelFrame(self.root, text="Menu")
        self.menu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.menu_listbox = tk.Listbox(self.menu_frame)
        self.menu_listbox.pack(fill=tk.BOTH, expand=True)

        self.danie_add = tk.Button(self.menu_frame, text="Dodaj Danie", command=self.dodaj_danie_okno)
        self.danie_add.pack()




        for danie in self.menu.dania:
            self.menu_listbox.insert(tk.END, str(danie))

    def dodaj_stolik(self):
        if not self.kelnerzy:
            messagebox.showwarning("Brak kelnerów", "Najpierw dodaj kelnerów!")
            return

        kelner_dialog = KelnerDialog(self.root, "Wybierz kelnera", self.kelnerzy)
        self.root.wait_window(kelner_dialog)

        kelner = kelner_dialog.wybrany_kelner
        if kelner is None:
            return

        numer_stolika = len(self.stoliki) + 1
        ilosc_osob = simpledialog.askinteger("Ilość osób", "Podaj ilość osób przy stoliku")
        if ilosc_osob is None or ilosc_osob < 1:
            messagebox.showerror("Niepoprawna ilość osób")
            return

        stolik = Stolik(numer_stolika, ilosc_osob)
        stolik.przypisz_kelnera(kelner)
        self.stoliki.append(stolik)

        if not self.menu.dania:
            messagebox.showwarning("Brak dań", "Najpierw dodaj dania do menu!")
            return

        self.odswiez_stoliki_frame()

        danie_dialog = DanieDialog(self.root, "Wybierz dania dla stolika", self.menu)
        if danie_dialog.wybrane_dania:
            for danie, ilosc in danie_dialog.wybrane_dania.items():
                stolik.dodaj_danie(danie, ilosc)

    def dodaj_kelnera(self):
        imie = simpledialog.askstring("Dodaj kelnera", "Podaj imię kelnera", parent=self.root)
        if imie:
            kelner = Kelner(imie)
            self.kelnerzy.append(kelner)
            self.odswiez_kelnerzy_listbox()
        else:
            messagebox.showwarning("Brak imienia", "Nie podano imienia kelnera.")

    def pokaz_stolik(self, stolik):
        StolikDialog(self.root, f"Stolik {stolik.numer_stolika}", stolik, self.menu)

    def odswiez_stoliki_frame(self):
        for widget in self.stoliki_listbox.winfo_children():
            widget.destroy()

        for stolik in self.stoliki:
            stolik_button = tk.Button(self.stoliki_listbox, text=f"Stolik {stolik.numer_stolika}",
                                      command=lambda s=stolik: self.pokaz_stolik(s))
            stolik_button.pack(fill=tk.X)

        self.stoliki_listbox.pack(fill=tk.BOTH, expand=True)

    def odswiez_kelnerzy_listbox(self):
        for widget in self.kelnerzy_listbox.winfo_children():
            widget.destroy()

        for kelner in self.kelnerzy:
            kelner_button = tk.Button(self.kelnerzy_listbox, text=str(kelner),
                                      command=lambda k=kelner: self.kelner_akcja(k))
            kelner_button.pack(fill=tk.X)

    def kelner_akcja(self, kelner):
        self.pokaz_stoliki_kelnera(kelner)

    def pokaz_stoliki_kelnera(self, kelner):
        top = tk.Toplevel(self.root)
        top.title(f"Stoliki przypisane do kelnera: {kelner}")

        stoliki_frame = tk.Frame(top)
        stoliki_frame.pack(fill=tk.BOTH, expand=True)

        for stolik in self.stoliki:
            if stolik.kelner == kelner:
                stolik_button = tk.Button(stoliki_frame, text=f"Stolik {stolik.numer_stolika}",
                                          command=lambda s=stolik: self.pokaz_stolik(s))
                stolik_button.pack(fill=tk.X)

    def dodaj_danie_okno(self):
        wybor_dania = simpledialog.askstring("Dodaj Danie", "Wybierz rodzaj dania (klasyczne / wegańskie):",
                                             initialvalue="klasyczne")
        if wybor_dania.lower() == "klasyczne":
            self.dodaj_danie()
        elif wybor_dania.lower() == "wegańskie":
            self.dodaj_danie_weganskie()

    def dodaj_danie(self):
        nazwa = simpledialog.askstring("Nazwa dania", "Podaj nazwę dania:")
        cena = simpledialog.askfloat("Cena dania", "Podaj cenę dania (PLN):")
        if nazwa and cena is not None:
            danie = Danie(nazwa, cena)
            self.menu.dodaj_danie(danie)
            self.menu_listbox.insert(tk.END, str(danie))

    def dodaj_danie_weganskie(self):
        nazwa = simpledialog.askstring("Nazwa dania", "Podaj nazwę dania:")
        cena = simpledialog.askfloat("Cena dania", "Podaj cenę dania (PLN):")
        skladniki = simpledialog.askstring("Składniki", "Podaj składniki (oddzielone przecinkiem):")
        if nazwa and cena is not None and skladniki:
            skladniki_lista = [skladnik.strip() for skladnik in skladniki.split(",")]
            danie = DanieWeganskie(nazwa, cena, skladniki_lista)
            self.menu.dodaj_danie(danie)
            self.menu_listbox.insert(tk.END, str(danie))

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplikacja(root)
    root.mainloop()






