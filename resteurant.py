

class Stolik:

    def __init__(self, numer_stolika, ilosc_osob):
        self.numer_stolika = numer_stolika
        self.ilosc_osob = ilosc_osob
        self.zamowienie = None
        self.kelner = None

    def zloz_zamowienie(self, zamowienie):
        self.zamowienie = zamowienie
        print(f"Zamówienie dla stolika {self.numer_stolika} zostało złożone przez kelnera {self.kelner}.")

    def przypisz_kelnera(self, kelner):
        self.kelner = kelner
        print(f"Stolik {self.numer_stolika} został przypisany do kelnera {self.kelner}.")

    def __str__(self):
        return f"Stolik {self.numer_stolika}: {self.ilosc_osob} osób, obsługiwany przez kelnera {self.kelner}"






class Kelner:
    def __init__(self, kod):
        self.kod = kod
        self.zalogowany = False
        self.przypisany_stolik = None

    def zaloguj(self, kod):
        if kod == self.kod:
            self.zalogowany = True
            print("Kelner zalogowany.")
        else:
            print("Błędny kod.")

    def wyloguj(self):
        self.zalogowany = False
        print("Kelner wylogowany.")

    def przypisz_stolik(self, stolik):
        if self.zalogowany:
            self.przypisany_stolik = stolik
            print(f"Stolik {stolik.numer_stolika} został przypisany do kelnera.")
        else:
            print("Kelner nie jest zalogowany.")

    def __str__(self):
        return f"Kelner: {self.kod}, zalogowany: {self.zalogowany}, przypisany stolik: {self.przypisany_stolik}"





class Danie:
    def __init__(self, nazwa, cena):
        self.nazwa = nazwa
        self.cena = cena

    def __str__(self):
        return f"{self.nazwa} - {self.cena} PLN"




class Menu:
    def __init__(self):
        self.dania = []

    def dodaj_danie(self, danie):
        if isinstance(danie, Danie):
            self.dania.append(danie)
        else:
            print("To nie jest obiekt klasy Danie!")

    def usun_danie(self, nazwa_dania):
        self.dania = [danie for danie in self.dania if danie.nazwa != nazwa_dania]

    def wyswietl_menu(self):
        return "\n".join(str(danie) for danie in self.dania)

    def znajdz_danie(self, nazwa_dania):
        for danie in self.dania:
            if danie.nazwa == nazwa_dania:
                return danie
        return None
