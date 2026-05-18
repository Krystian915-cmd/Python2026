"""
Moduł: gui
Zarządza interfejsem graficznym.
Implementuje podział ról: Administrator (wymaga PIN) i Klient (Nowy / Zarejestrowany).
"""

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk 
import customers
import addresses
import monitor
import products  # Dodany import, aby handle_add_product działało poprawnie

# Zmienne globalne do zarządzania sesją
ADMIN_PIN = "1234"  # Prosty PIN do obrony projektu
current_customer_id = None  # Przechowuje ID zalogowanego klienta


def start_app():
    root = tk.Tk()
    root.title("Sklep Żabka Online")
    root.geometry("450x650")  # Delikatnie zwiększona wysokość, by zmieścić logo

    # ==========================================
    # LOGIKA PRZEŁĄCZANIA EKRANÓW
    # ==========================================
    def hide_all_frames():
        """Chowa wszystkie ekrany, żeby zrobić miejsce na nowy."""
        frame_main.pack_forget()
        frame_admin_login.pack_forget()
        frame_admin_panel.pack_forget()
        frame_customer_menu.pack_forget()
        frame_new_customer.pack_forget()
        frame_reg_customer.pack_forget()
        frame_shopping.pack_forget()

    def show_frame(frame):
        """Chowa wszystko i wyświetla wybraną ramkę."""
        hide_all_frames()
        frame.pack(fill="both", expand=True, pady=20)

    # ==========================================
    # TWORZENIE RAMEK (EKRANÓW)
    # ==========================================
    frame_main = tk.Frame(root)
    frame_admin_login = tk.Frame(root)
    frame_admin_panel = tk.Frame(root)
    frame_customer_menu = tk.Frame(root)
    frame_new_customer = tk.Frame(root)
    frame_reg_customer = tk.Frame(root)
    frame_shopping = tk.Frame(root)

    # ==========================================
    # EKRAN 1: MENU GŁÓWNE
    # ==========================================
    
    # ------------------------------------------
    # SEKCJA: DODAWANIE LOGO NA EKRANIE GŁÓWNYM
    # ------------------------------------------
    try:
        # Wczytanie pliku - upewnij się, że plik 'zabka_logo.png' jest w tym samym folderze!
        img_raw = Image.open("zabka_logo.png")
        img_resized = img_raw.resize((140, 140))  # Dobrana wielkość pasująca do okna
        img_logo = ImageTk.PhotoImage(img_resized)
        
        lbl_logo = tk.Label(frame_main, image=img_logo)
        lbl_logo.image = img_logo  # Wymagane zakotwiczenie referencji w pamięci
        lbl_logo.pack(pady=15)
    except FileNotFoundError:
        # Rezerwowy komunikat tekstowy, jeśli plik z obrazkiem zniknie
        tk.Label(frame_main, text="[ Zielona Żabka ]", fg="green", font=("Arial", 12, "italic")).pack(pady=15)
    # ------------------------------------------

    tk.Label(frame_main, text="WITAJ W ŻABCE ONLINE", font=("Arial", 16, "bold")).pack(pady=15)
    tk.Label(frame_main, text="Wybierz swoją rolę:", font=("Arial", 12)).pack(pady=10)

    tk.Button(frame_main, text="Jestem Administratorem", width=25, height=2, bg="lightblue",
              command=lambda: show_frame(frame_admin_login)).pack(pady=10)
    tk.Button(frame_main, text="Jestem Klientem", width=25, height=2, bg="lightgreen",
              command=lambda: show_frame(frame_customer_menu)).pack(pady=10)
    
    # ==========================================
    # EKRAN 2: LOGOWANIE ADMINA
    # ==========================================
    tk.Label(frame_admin_login, text="LOGOWANIE ADMINISTRATORA", font=("Arial", 14, "bold")).pack(pady=20)
    tk.Label(frame_admin_login, text="Podaj PIN:").pack()

    entry_pin = tk.Entry(frame_admin_login, show="*")  # show="*" ukrywa wpisywane znaki
    entry_pin.pack(pady=5)

    def verify_pin():
        if entry_pin.get() == ADMIN_PIN:
            entry_pin.delete(0, tk.END)
            show_frame(frame_admin_panel)
        else:
            messagebox.showerror("Błąd", "Nieprawidłowy PIN!")
            entry_pin.delete(0, tk.END)

    tk.Button(frame_admin_login, text="Zaloguj", command=verify_pin, bg="orange").pack(pady=10)
    tk.Button(frame_admin_login, text="Powrót", command=lambda: show_frame(frame_main)).pack(pady=5)

    # ==========================================
    # EKRAN 3: PANEL ADMINISTRATORA
    # ==========================================
    tk.Label(frame_admin_panel, text="PANEL ADMINISTRATORA", font=("Arial", 14, "bold")).pack(pady=10)

    # Dodawanie produktu
    frame_add_prod = tk.LabelFrame(frame_admin_panel, text="Dodaj Produkt")
    frame_add_prod.pack(pady=5, fill="x", padx=20)

    tk.Label(frame_add_prod, text="ID:").grid(row=0, column=0)
    entry_prod_id = tk.Entry(frame_add_prod, width=10)
    entry_prod_id.grid(row=0, column=1)

    tk.Label(frame_add_prod, text="Nazwa:").grid(row=0, column=2)
    entry_prod_name = tk.Entry(frame_add_prod, width=15)
    entry_prod_name.grid(row=0, column=3)

    tk.Label(frame_add_prod, text="Cena:").grid(row=1, column=0)
    entry_prod_price = tk.Entry(frame_add_prod, width=10)
    entry_prod_price.grid(row=1, column=1)

    tk.Label(frame_add_prod, text="Ilość:").grid(row=1, column=2)
    entry_prod_qty = tk.Entry(frame_add_prod, width=15)
    entry_prod_qty.grid(row=1, column=3)

    def handle_add_product():
        try:
            products.add_product(int(entry_prod_id.get()), entry_prod_name.get(),
                                 float(entry_prod_price.get()), int(entry_prod_qty.get()))
            messagebox.showinfo("Sukces", "Zapisano produkt w bazie!")
        except:
            messagebox.showerror("Błąd", "Sprawdź poprawność danych!")

    tk.Button(frame_add_prod, text="Dodaj", command=handle_add_product).grid(row=2, column=0, columnspan=4, pady=5)

    # Usuwanie Klienta
    frame_del_cust = tk.LabelFrame(frame_admin_panel, text="Usuń Klienta (po ID)")
    frame_del_cust.pack(pady=5, fill="x", padx=20)
    entry_del_cust = tk.Entry(frame_del_cust)
    entry_del_cust.pack(side="left", padx=10, pady=5)
    tk.Button(frame_del_cust, text="Usuń", command=lambda: customers.delete_customer(entry_del_cust.get())).pack(
        side="left")

    # Pokaż statystyki
    def show_stats():
        messagebox.showinfo("Statystyki", monitor.generate_statistics_report())

    tk.Button(frame_admin_panel, text="📊 Statystyki Magazynu", command=show_stats, bg="gold").pack(pady=10)
    tk.Button(frame_admin_panel, text="Wyloguj (Powrót)", command=lambda: show_frame(frame_main)).pack(pady=10)

    # ==========================================
    # EKRAN 4: MENU KLIENTA
    # ==========================================
    tk.Label(frame_customer_menu, text="STREFA KLIENTA", font=("Arial", 14, "bold")).pack(pady=20)

    tk.Button(frame_customer_menu, text="Jestem Nowym Klientem (Rejestracja)", width=35, height=2,
              command=lambda: show_frame(frame_new_customer)).pack(pady=10)
    tk.Button(frame_customer_menu, text="Mam już kartę stałego klienta (Logowanie)", width=35, height=2,
              command=lambda: show_frame(frame_reg_customer)).pack(pady=10)
    tk.Button(frame_customer_menu, text="Powrót", command=lambda: show_frame(frame_main)).pack(pady=20)

    # ==========================================
    # EKRAN 5: REJESTRACJA NOWEGO KLIENTA
    # ==========================================
    tk.Label(frame_new_customer, text="REJESTRACJA", font=("Arial", 14, "bold")).pack(pady=10)

    tk.Label(frame_new_customer, text="Imię:").pack()
    entry_new_name = tk.Entry(frame_new_customer)
    entry_new_name.pack()

    tk.Label(frame_new_customer, text="Nazwisko:").pack()
    entry_new_surname = tk.Entry(frame_new_customer)
    entry_new_surname.pack()

    tk.Label(frame_new_customer, text="Miasto:").pack()
    entry_new_city = tk.Entry(frame_new_customer)
    entry_new_city.pack()

    tk.Label(frame_new_customer, text="Ulica:").pack()
    entry_new_street = tk.Entry(frame_new_customer)
    entry_new_street.pack()

    def handle_register():
        global current_customer_id
        name, surname = entry_new_name.get(), entry_new_surname.get()
        city, street = entry_new_city.get(), entry_new_street.get()

        if name and surname and city and street:
            new_id = customers.register_customer(name, surname)
            addresses.update_customer_address(new_id, city, street)
            current_customer_id = new_id  # Automatyczne "zalogowanie" po rejestracji

            messagebox.showinfo("Sukces",
                                f"Zarejestrowano!\nTwoje ID klienta to: {new_id}\nZapamiętaj je do logowania!")
            lbl_shopping_user.config(text=f"Zalogowano jako ID: {current_customer_id}")
            show_frame(frame_shopping)
        else:
            messagebox.showwarning("Błąd", "Wypełnij wszystkie 4 pola!")

    tk.Button(frame_new_customer, text="Załóż konto i przejdź do zakupów", command=handle_register,
              bg="lightgreen").pack(pady=15)
    tk.Button(frame_new_customer, text="Powrót", command=lambda: show_frame(frame_customer_menu)).pack()

    # ==========================================
    # EKRAN 6: LOGOWANIE ZAREJESTROWANEGO KLIENTA
    # ==========================================
    tk.Label(frame_reg_customer, text="LOGOWANIE KLIENTA", font=("Arial", 14, "bold")).pack(pady=20)
    tk.Label(frame_reg_customer, text="Podaj swoje ID:").pack()
    entry_login_id = tk.Entry(frame_reg_customer)
    entry_login_id.pack(pady=10)

    def handle_login():
        global current_customer_id
        try:
            cid = int(entry_login_id.get())
            # Sprawdzamy czy ID istnieje w bazie
            df = customers.load_csv(customers.CUSTOMERS_FILE, ["ID"])
            if cid in df["ID"].values:
                current_customer_id = cid
                lbl_shopping_user.config(text=f"Zalogowano jako ID: {current_customer_id}")
                show_frame(frame_shopping)
            else:
                messagebox.showerror("Błąd", "Nie znaleziono takiego ID w bazie!")
        except ValueError:
            messagebox.showerror("Błąd", "ID musi być liczbą!")

    tk.Button(frame_reg_customer, text="Zaloguj", command=handle_login, bg="lightblue").pack(pady=10)
    tk.Button(frame_reg_customer, text="Powrót", command=lambda: show_frame(frame_customer_menu)).pack()

    # ==========================================
    # EKRAN 7: ZAKUPY KLIENTA (Wiele produktów naraz)
    # ==========================================
    tk.Label(frame_shopping, text="🛒 SKLEP ŻABKA", font=("Arial", 16, "bold")).pack(pady=10)
    lbl_shopping_user = tk.Label(frame_shopping, text="Zalogowano jako ID: Brak", fg="gray")
    lbl_shopping_user.pack(pady=5)

    tk.Label(frame_shopping, text="Produkty (rozdziel przecinkiem np. Woda, Baton):").pack()
    entry_buy_name = tk.Entry(frame_shopping, width=30)
    entry_buy_name.pack()

    tk.Label(frame_shopping, text="Ilości sztuk (rozdziel przecinkiem np. 2, 1):").pack()
    entry_buy_qty = tk.Entry(frame_shopping, width=30)
    entry_buy_qty.pack(pady=5)

    def handle_buy():
        global current_customer_id
        try:
            # 1. Pobieramy tekst i dzielimy go za pomocą przecinków na listy
            names_raw = entry_buy_name.get().split(',')
            qtys_raw = entry_buy_qty.get().split(',')
            
            # 2. Usuwamy zbędne spacje z nazw (np. " Baton" -> "Baton") i rzutujemy ilości na int
            names = [name.strip() for name in names_raw]
            qtys = [int(qty.strip()) for qty in qtys_raw]
            
            # 3. Sprawdzamy czy klient podał tyle samo ilości co produktów
            if len(names) != len(qtys):
                messagebox.showerror("Błąd", "Liczba produktów musi odpowiadać liczbie podanych ilości!")
                return
                
            # 4. Łączymy w krotki za pomocą funkcji zip: [("Woda", 2), ("Baton", 1)]
            items_to_buy = list(zip(names, qtys))
            
            # 5. Używamy gwiazdki (*), aby rozpakować listę krotek prosto do Twojego dekoratora!
            customers.buy_product(current_customer_id, *items_to_buy)
            
            messagebox.showinfo("Koszyk", "Próba zakupu zrealizowana!\nSprawdź konsolę, aby zobaczyć, czy starczyło towaru w magazynie.")
            entry_buy_name.delete(0, tk.END)
            entry_buy_qty.delete(0, tk.END)
            
        except ValueError:
            messagebox.showerror("Błąd", "W polu 'Ilości' muszą znajdować się wyłącznie cyfry oddzielone przecinkami!")

    tk.Button(frame_shopping, text="KUPUJĘ!", command=handle_buy, bg="orange", width=20, height=2).pack(pady=15)
    
    def handle_logout():
        global current_customer_id
        current_customer_id = None
        show_frame(frame_main)
        
    tk.Button(frame_shopping, text="Zakończ zakupy i Wyloguj", command=handle_logout).pack()

    # Start aplikacji - pokaż jako pierwsze Menu Główne
    show_frame(frame_main)
    root.mainloop()


if __name__ == "__main__":
    start_app()