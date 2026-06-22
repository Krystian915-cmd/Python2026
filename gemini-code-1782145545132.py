import os

class Prostokat:
    def __init__(self, a=10, b=10):
        self.a = a
        self.b = b

    def poleprostokata(self):
        return self.a * self.b

    def __str__(self):
        return f"Prostokąt o bokach {self.a} i {self.b}"

    # Metoda magiczna __add__ (wymagana w niektórych wariantach do sumowania pól)
    def __add__(self, other):
        if isinstance(other, Prostokat):
            return self.poleprostokata() + other.poleprostokata()
        return NotImplemented

    # Metoda zmieniająca długość boku
    def zmien_bok(self, nowy_a):
        self.a = nowy_a


class Prostopadloscian(Prostokat):
    def __init__(self, a=10, b=10, h=1):
        # Dziedziczenie pól za pomocą super()
        super().__init__(a, b)
        # Ustawienie domyślnej wartości dla wysokości (H=1)
        self.h = h

    def poleprostopadloscianu(self):
        # Oblicza pole powierzchni korzystając z metody rodzica: poleprostokata()
        pole_podstawy = self.poleprostokata()
        pole_boczne_1 = self.a * self.h
        pole_boczne_2 = self.b * self.h
        return 2 * pole_podstawy + 2 * pole_boczne_1 + 2 * pole_boczne_2


# Szybki test działania klas (Zadanie 1a podpunkt c: A=10, B=10, H=10)
if __name__ == "__main__":
    bryla = Prostopadloscian(a=10, b=10, h=10)
    print(f"Pole powierzchni prostopadłościanu: {bryla.poleprostopadloscianu()}")