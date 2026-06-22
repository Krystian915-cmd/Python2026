import math
import unittest

# --- DEKORATOR (Wymagany w wariancie 2b z przedostatniej kartki) ---
def dekoruj_logowanie(funkcja):
    def wrapper(*args, **kwargs):
        wynik = funkcja(*args, **kwargs)
        # Dynamiczne wypisywanie komunikatów w zależności od tego, co się stało
        if "iloczyn" in str(funkcja.__name__) or len(args) > 1:
            print("Liczę iloczyn liczb")
        else:
            print("Liczę sumę liczb")
        return wynik
    return wrapper


# --- FUNKCJE WIELU ZMIENNYCH ---

@dekoruj_logowanie
def oblicz_wariant_a(*args):
    """Funkcja obsługująca warianty z podawaniem list lub pojedynczych liczb"""
    if len(args) == 1:
        arg = args[0]
        # Jeśli podano pojedynczą liczbę -> pierwiastek
        if isinstance(arg, (int, float)):
            return math.sqrt(arg)
        # Jeśli podano String -> komunikat
        elif isinstance(arg, str):
            return "nie jestem liczbą"
        # Jeśli podano listę (Wariant 2b z drugiej kartki) -> potęga parzystych
        elif isinstance(arg, list):
            # Użycie lambda + filter oraz map
            parzyste = filter(lambda x: x % 2 == 0, arg)
            return list(map(lambda x: x ** 2, parzyste))
            
    # Jeśli podano więcej niż 1 argument i dane są numeryczne
    if len(args) > 1 and all(isinstance(x, (int, float)) for x in args):
        # Obliczanie iloczynu pętlą for
        iloczyn = 1
        for liczba in args:
            iloczyn *= list(args)[args.index(liczba)] # demonstracja pętli
        return iloczyn
        
    return None


@dekoruj_logowanie
def oblicz_wariant_b(*args, **kwargs):
    """Funkcja obsługująca pętle while oraz parametry nazwane (**kwargs)"""
    # Jeśli argumenty mają nazwy (**kwargs)
    if kwargs:
        liczby = list(kwargs.values())
        iloczyn = 1
        i = 0
        # Użycie pętli while do obliczenia iloczynu
        while i < len(liczby):
            iloczyn *= liczby[i]
            i += 1
        return iloczyn

    # Jeśli argumenty NIE mają nazw (*args) -> sumujemy nieparzyste przez filter
    if args:
        nieparzyste = list(filter(lambda x: x % 2 != 0, args))
        return sum(nieparzyste)


# --- TESTY JEDNOSTKOWE (unittest) ---
class TestFunkcji(unittest.TestCase):
    def test_pierwiastek_i_string(self):
        self.assertEqual(oblicz_wariant_a(9), 3.0)
        self.assertEqual(oblicz_wariant_a("test"), "nie jestem liczbą")

    def test_lista_i_lambda(self):
        self.assertEqual(oblicz_wariant_a([1, 2, 3, 4]), [4, 16]) # parzyste do kwadratu

    def test_iloczyn_while(self):
        self.assertEqual(oblicz_wariant_b(a=2, b=3, c=4), 24)


if __name__ == "__main__":
    unittest.main()