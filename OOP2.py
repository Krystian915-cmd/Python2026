import os
import math
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import unittest

# ==========================================
# ZADANIE 1: KLASY, DZIEDZICZENIE I TOOLS
# ==========================================

class Plik1:
    # b. Pole klasy (wspólne dla wszystkich instancji)
    file_number = 1

    # a. Konstruktor z domyślną wartością "NewFile"
    def __init__(self, nazwa_pliku="NewFile"):
        self.nazwa_pliku = nazwa_pliku

    # c. Metoda magiczna zwracająca nazwę pliku przy wyświetlaniu
    def __str__(self):
        return f"Nazwa pliku: {self.nazwa_pliku}"

    # d. Metoda prywatna zmieniająca nazwę pliku
    def __zmien_nazwe(self, nowa_nazwa):
        self.nazwa_pliku = nowa_nazwa


class Plik2(Plik1):
    def __init__(self, nazwa_pliku="NewFile", nazwa_folderu="moje_pliki"):
        # a. Dziedziczenie pól konstruktora przy użyciu super()
        super().__init__(nazwa_pliku)
        # Dodatkowe pole z nazwą folderu
        self.nazwa_folderu = nazwa_folderu

    # b. Metoda zapisująca tekst wraz z dokumentacją (docstring)
    def zapisz_tekst(self, tekst):
        """
        Zapisuje podany przez użytkownika tekst do pliku we wskazanym folderze.
        Jeśli folder nie istnieje, zostanie automatycznie utworzony.
        """
        if not os.path.exists(self.nazwa_folderu):
            os.makedirs(self.nazwa_folderu)
            
        sciezka = os.path.join(self.nazwa_folderu, self.nazwa_pliku)
        with open(sciezka, "w", encoding="utf-8") as plik:
            plik.write(tekst)
        print(f"Zapisano w: {sciezka}")


class Tools:
    def oblicz(self, *args, **kwargs):
        # Sytuacja 1: Gdy przekazano parametry nazwane (**kwargs) -> suma wartości
        if kwargs:
            suma = 0
            for klucz, wartosc in kwargs.items():
                suma += wartosc
            return suma
            
        # Sytuacja 2: Gdy przekazano argumenty pozycyjne (*args) -> iloczyn parzystych liczb
        if args:
            # Filtrujemy tylko liczby parzyste za pomocą filter()
            liczby_parzyste = list(filter(lambda x: isinstance(x, (int, float)) and x % 2 == 0, args))
            if not liczby_parzyste:
                return 0
            # Obliczamy iloczyn przefiltrowanych liczb
            return math.prod(liczby_parzyste)
            
        return None

# ==========================================
# ZADANIE 2: INTERFEJS TKINTER + PANDAS
# ==========================================

class TitanicAppKlasy:
    def __init__(self, root):
        self.root = root
        self.root.title("Statystyki Titanica - Klasy")
        self.root.geometry("400x280")
        
        # Zmienna przechowująca wybór klasy (1, 2 lub 3)
        self.wybrana_klasa = tk.IntVar(value=1)
        self.ostatni_wynik = None

        # Try-Except przy ładowaniu pliku excel / csv
        try:
            self.df = pd.read_excel("titanic_train.xlsx")
        except FileNotFoundError:
            try:
                self.df = pd.read_csv("titanic_train.csv")
            except FileNotFoundError:
                messagebox.showerror("Błąd", "Nie znaleziono pliku danych (titanic_train.xlsx / csv)!")
                self.root.destroy()
                return

        self.stworz_interfejs()

    def stworz_interfejs(self):
        tk.Label(self.root, text="Wybierz klasę pasażerską:", font=("Arial", 12, "bold")).pack(pady=10)

        # Kontrolki Radiobutton dla klas 1, 2, 3
        tk.Radiobutton(self.root, text="Klasa 1", variable=self.wybrana_klasa, value=1).pack()
        tk.Radiobutton(self.root, text="Klasa 2", variable=self.wybrana_klasa, value=2).pack()
        tk.Radiobutton(self.root, text="Klasa 3", variable=self.wybrana_klasa, value=3).pack()

        # Przycisk OK
        btn_ok = tk.Button(self.root, text="OK", command=self.oblicz_wiek, bg="#4CAF50", fg="white")
        btn_ok.pack(pady=15)

        self.lbl_wynik = tk.Label(self.root, text="Wynik: -", font=("Arial", 11))
        self.lbl_wynik.pack(pady=5)

        # Przycisk Zapisz
        btn_zapisz = tk.Button(self.root, text="Zapisz", command=self.zapisz_do_pliku, bg="#008CBA", fg="white")
        btn_zapisz.pack(pady=5)

    def oblicz_wiek(self):
        klasa = self.wybrana_klasa.get()
        # Filtrowanie po klasie ORAZ wieku starszym niż 30 lat
        filtrowani = self.df[(self.df['Pclass'] == klasa) & (self.df['Age'] > 30)]
        
        self.ostatni_wynik = f"Klasa {klasa}, wiek > 30 lat: {len(filtrowani)} pasażerów"
        self.lbl_wynik.config(text=self.ostatni_wynik)

    def zapisz_do_pliku(self):
        if self.ostatni_wynik is None:
            messagebox.showwarning("Uwaga", "Najpierw kliknij OK!")
            return
        with open("wynik_klasy.txt", "w", encoding="utf-8") as f:
            f.write(self.ostatni_wynik + "\n")
        messagebox.showinfo("Zapisano", "Zapisano do pliku wynik_klasy.txt")

# ==========================================
# LOGIKA DO TESTU JEDNOSTKOWEGO I TESTY
# ==========================================

def policz_pasazerow_testowa(dataframe, klasa):
    return len(dataframe[(dataframe['Pclass'] == klasa) & (dataframe['Age'] > 30)])

