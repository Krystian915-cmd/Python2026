import math
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import unittest

# ==========================================
# ZADANIE 1: KLASY, DZIEDZICZENIE I TOOLS
# ==========================================

class Logowanie:
    # a. Prywatne pole klasy (zaczyna się od __)
    __pin = '0000'

    # b. Konstruktor z domyślną wartością dla loginu
    def __init__(self, login="admin", haslo="1234"):
        self.login = login
        self.haslo = haslo

    # c. Metoda magiczna (wywoływana automatycznie przy print())
    def __str__(self):
        return f"Login: {self.login}, Hasło: {self.haslo}, PIN: {Logowanie.__pin}"

    # d. Metoda zmieniająca prywatny pin
    def zmienpin(self, nowy_pin):
        Logowanie.__pin = nowy_pin


class LogowanieStudent(Logowanie):
    def __init__(self, login="admin", haslo="1234", imie="", nazwisko=""):
        # Dziedziczenie pola login za pomocą super()
        super().__init__(login, haslo)
        # 2 dodatkowe pola
        self.imie = imie
        self.nazwisko = nazwisko

    # Prywatna metoda (zaczyna się od __) zmieniająca dane
    def __zmiendane(self, nowe_imie, nowe_nazwisko, nowe_haslo):
        self.imie = nowe_imie
        self.nazwisko = nowe_nazwisko
        self.haslo = nowe_haslo


class Tools:
    def oblicz(self, *args, **kwargs):
        """
        Metoda sprawdza typ argumentów pozycyjnych (*args).
        Jeśli to Stringi -> powiększa litery.
        Jeśli parzyste liczby -> oblicza ich pierwiastki.
        """
        if args:
            # Sytuacja 1: Jeśli wszystkie argumenty to napisy (String)
            if all(isinstance(x, str) for x in args):
                return [x.upper() for x in args]
            
            # Sytuacja 2: Jeśli wszystkie argumenty są numeryczne i parzyste
            if all(isinstance(x, (int, float)) and x % 2 == 0 for x in args):
                # map() aplikuje funkcję math.sqrt do każdego elementu z args
                return list(map(math.sqrt, args))
                
        return None

# ==========================================
# ZADANIE 2: INTERFEJS TKINTER + PANDAS
# ==========================================
import tkinter as tk
from tkinter import messagebox
import pandas as pd

class Titanic:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x400")
        self.root.title("Statystyka")

        # Zmienna Tkinter dla Radiobuttonów
        self.wybrana_klasa = tk.IntVar(value=1)

        # Zmienna do przechowywania wyniku (zamiast zadna_klasa)
        self.ostatni_wynik = None
        
        # Obsługa wyjątków
        try:
            self.df = pd.read_csv("titanic_train.csv") # Wpisz właściwą nazwę pliku
        except FileNotFoundError:
            try:
                self.df = pd.read_excel("titanic_train.xlsx")
            except FileNotFoundError:
                messagebox.showerror("Blad", "Nie znaleziono pliku!")
                self.root.destroy() # Dodane nawiasy ()
                return
            
        self.stworz_interfejs()

    def stworz_interfejs(self):
        # Zmieniono 'self' na 'self.root' jako rodzica komponentów
        tk.Label(self.root, text="Wybierz klase").pack(pady=10)

        # Poprawiono 'variable' na self.wybrana_klasa i dodano 3 klasę
        tk.Radiobutton(self.root, text="1 klasa", variable=self.wybrana_klasa, value=1).pack()
        tk.Radiobutton(self.root, text="2 klasa", variable=self.wybrana_klasa, value=2).pack()
        tk.Radiobutton(self.root, text="3 klasa", variable=self.wybrana_klasa, value=3).pack()
        
        btn_OK = tk.Button(self.root, text="OK", command=self.oblicz_ilosc)
        btn_OK.pack(pady=5)
    
        self.lbl_wynik = tk.Label(self.root, text="wynik: -")
        self.lbl_wynik.pack(pady=5)

        btn_Zapisz = tk.Button(self.root, text="Zapisz", command=self.zapisz_wynik)
        btn_Zapisz.pack(pady=5)

    def oblicz_ilosc(self):
        klasa = self.wybrana_klasa.get()
        
        # Poprawione filtrowanie Pandas - każdy warunek w osobnych nawiasach ()
        filtrowanie = self.df[(self.df['Pclass'] == klasa) & (self.df['Age'] > 30)]
        liczba = len(filtrowanie)
        
        # Dodano brakujący znak =
        self.ostatni_wynik = f"klasa {klasa} ma dokladnie {liczba} pasazerow starszych niz 30 lat"
        self.lbl_wynik.config(text=self.ostatni_wynik)

    def zapisz_wynik(self):
        # Sprawdzamy self.ostatni_wynik
        if self.ostatni_wynik is None:
            messagebox.showwarning('Uwaga', 'Najpierw kliknij OK!')
            return
            
        with open("wynik_klasy.txt", "w", encoding="utf-8") as p:
            p.write(self.ostatni_wynik + "\n")
        messagebox.showinfo('Sukces', 'Zapisano pomyslnie')

# Uruchomienie aplikacji
if __name__ == "__main__":
    root = tk.Tk()
    app = Titanic(root)
    root.mainloop()