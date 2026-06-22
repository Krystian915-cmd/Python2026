import tkinter as tk
from tkinter import messagebox
import pandas as pd
import pickle
import os

class KalkulatorAplikacja:
    def __init__(self, root):
        self.root = root
        self.root.title("Zaawansowany Kalkulator / Statystyka")
        self.root.geometry("450x400")

        # Zmienna do wyboru operacji (dodawanie / dzielenie)
        self.operacja = tk.StringVar(value="dodawanie")
        self.ostatni_wynik = None

        # Wczytywanie bazy danych filmów z try-except (wymóg z kartek)
        try:
            # Tworzymy plik testowy w locie na wypadek gdyby go nie było w folderze
            if not os.path.exists("movies.csv"):
                df_temp = pd.DataFrame({'title': ['Film A', 'Film B'], 'budget': [100, 200], 'director': ['Jan', 'Anna']})
                df_temp.to_csv("movies.csv", index=False)
                
            self.df = pd.read_csv("movies.csv")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie udało się załadować bazy filmów:\n{e}")
            self.root.destroy()
            return

        self.stworz_interfejs()

    def stworz_interfejs(self):
        # Dokumentacja wewnątrz funkcji (wymóg: dokumentacja dla 1 z funkcji)
        """Generuje wszystkie elementy graficzne interfejsu użytkownika."""
        
        # 1. Suwak dla pierwszej liczby (Scale)
        tk.Label(self.root, text="Liczba 1 (Suwak):").pack()
        self.suwak = tk.Scale(self.root, from_=1, to=100, orient=tk.HORIZONTAL)
        self.suwak.pack()

        # 2. Okienko edycyjne dla drugiej liczby (Entry)
        tk.Label(self.root, text="Liczba 2 (Okno edycyjne):").pack(pady=5)
        self.pole_tekstowe = tk.Entry(self.root)
        self.pole_tekstowe.insert(0, "10") # wartość domyślna
        self.pole_tekstowe.pack()

        # 3. Wybór operacji (Radiobuttony)
        tk.Label(self.root, text="Wybierz operację:", font=("Arial", 10, "bold")).pack(pady=10)
        tk.Radiobutton(self.root, text="Dodawanie", variable=self.operacja, value="dodawanie").pack()
        tk.Radiobutton(self.root, text="Dzielenie", variable=self.operacja, value="dzielenie").pack()

        # Przycisk OK
        btn_ok = tk.Button(self.root, text="OK", command=self.oblicz, bg="green", fg="white")
        btn_ok.pack(pady=10)

        # Wyświetlanie wyniku
        self.lbl_wynik = tk.Label(self.root, text="Wynik: -", font=("Arial", 11, "bold"))
        self.lbl_wynik.pack(pady=5)

        # Przycisk Zapisz
        btn_zapisz = tk.Button(self.root, text="Zapisz", command=self.zapisz, bg="blue", fg="white")
        btn_zapisz.pack(pady=5)

    def oblicz(self):
        # Obsługa wyjątków (try-except) podczas obliczeń matematycznych
        try:
            liczba1 = float(self.suwak.get())
            liczba2 = float(self.pole_tekstowe.get())
            typ = self.operacja.get()

            if typ == "dodawanie":
                wynik = liczba1 + liczba2
            elif typ == "dzielenie":
                if liczba2 == 0:
                    raise ZeroDivisionError("Nie dziel przez zero!")
                wynik = liczba1 / liczba2

            self.ostatni_wynik = wynik
            self.lbl_wynik.config(text=f"Wynik: {wynik}", fg="green")

        except ValueError:
            messagebox.showerror("Błąd", "W polu edycyjnym musisz podać poprawną liczbę!")
        except ZeroDivisionError as e:
            messagebox.showerror("Błąd matematyczny", str(e))

    def zapisz(self):
        if self.ostatni_wynik is None:
            messagebox.showwarning("Uwaga", "Brak wyniku do zapisania!")
            return

        # Zapis do pliku tekstowego oraz formatu PICKLE (spełnia oba warianty zadań)
        try:
            # Zwykły zapis tekstowy
            with open("wynik_kalkulatora.txt", "w", encoding="utf-8") as f:
                f.write(f"Ostatni wynik: {self.ostatni_wynik}\n")

            # Zapis obiektowy przez Pickle (wymagany na ostatniej kartce)
            with open("wynik.pickle", "wb") as pf:
                pickle.dump(self.ostatni_wynik, pf)

            messagebox.showinfo("Sukces", "Wynik zapisany poprawnie (TXT oraz PICKLE)!")
        except Exception as e:
            messagebox.showerror("Błąd zapisu", f"Nie udało się zapisać pliku: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = KalkulatorAplikacja(root)
    root.mainloop()