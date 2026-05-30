import tkinter as tk
from tkinter import messagebox
import math
from src.swiat.Swiat import Swiat

# Tutaj powinieneś zaimportować swoje klasy backendowe, np:
# from swiat_hex import SwiatHex
# from swiat_siatka import SwiatSiatka
# from menedzer_zapisu import MenedzerZapisu
# from rejestr_gatunkow import RejestrGatunkow

class OknoPowitalne:
    def __init__(self, root):
        self.root = root
        self.root.title("Wirtualny Świat - Python Edition")
        self.root.geometry("400x300")

        # Wyśrodkowanie okna na ekranie
        self.root.eval('tk::PlaceWindow . center')

        self.swiat = None
        self.zbuduj_panel_powitalny()

    def zbuduj_panel_powitalny(self):
        # Tytuł
        lbl_tytul = tk.Label(self.root, text="WIRTUALNY ŚWIAT", font=("Arial", 24, "bold"))
        lbl_tytul.pack(pady=20)

        # Wybór planszy (Radio Buttons)
        self.typ_planszy = tk.StringVar(value="Hex")
        ramka_radio = tk.Frame(self.root)
        ramka_radio.pack()
        tk.Radiobutton(ramka_radio, text="Plansza Hex", variable=self.typ_planszy, value="Hex").pack(side=tk.LEFT)
        tk.Radiobutton(ramka_radio, text="Plansza Siatka", variable=self.typ_planszy, value="Siatka").pack(side=tk.LEFT)

        # Pola do wpisywania rozmiarów
        ramka_rozmiar = tk.Frame(self.root)
        ramka_rozmiar.pack(pady=15)

        tk.Label(ramka_rozmiar, text="Szerokość (X):").grid(row=0, column=0, padx=5)
        self.pole_x = tk.Entry(ramka_rozmiar, width=5)
        self.pole_x.insert(0, "20")
        self.pole_x.grid(row=0, column=1)

        tk.Label(ramka_rozmiar, text="Wysokość (Y):").grid(row=1, column=0, padx=5)
        self.pole_y = tk.Entry(ramka_rozmiar, width=5)
        self.pole_y.insert(0, "20")
        self.pole_y.grid(row=1, column=1)

        # Przyciski akcji
        ramka_przyciski = tk.Frame(self.root)
        ramka_przyciski.pack(pady=10)
        tk.Button(ramka_przyciski, text="Start gry!", command=self.start_gry, bg="lightgreen").pack(side=tk.LEFT,
                                                                                                    padx=10)
        tk.Button(ramka_przyciski, text="Wczytaj Grę", command=self.wczytaj_gre, bg="lightblue").pack(side=tk.LEFT,
                                                                                                      padx=10)

    def start_gry(self):
        size_x = int(self.pole_x.get())
        size_y = int(self.pole_y.get())

        if self.typ_planszy.get() == "Hex":
            self.swiat = SwiatHex(size_x, size_y)
        else:
            self.swiat = SwiatSiatka(size_x, size_y)

        self.swiat.generuj_plansze()
        self.otworz_glowne_okno()

    def wczytaj_gre(self):
        # self.swiat = MenedzerZapisu.wczytaj_gre()
        self.otworz_glowne_okno()

    def otworz_glowne_okno(self):
        # Niszczymy obecne okno (powitalne) i tworzymy okno gry
        for widget in self.root.winfo_children():
            widget.destroy()
        GlowneOkno(self.root, self.swiat)


class GlowneOkno:
    def __init__(self, root, swiat):
        self.root = root
        self.swiat = swiat

        self.root.title("Wirtualny Świat")
        self.root.state('zoomed')  # Maksymalizacja okna na start

        self.zbuduj_panel_sterowania()
        self.zbuduj_panel_logow()

        # Wybór odpowiedniego płótna (Canvas)
        if self.swiat.czy_hex():
            self.panel_gry = PanelGryHex(self.root, self.swiat, self)
        else:
            self.panel_gry = PanelGrySiatka(self.root, self.swiat, self)

        self.panel_gry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.panel_gry.odswiez()

    def zbuduj_panel_sterowania(self):
        panel_kontroli = tk.Frame(self.root, bg="#eaeaea", pady=10)
        panel_kontroli.pack(side=tk.BOTTOM, fill=tk.X)

        tk.Button(panel_kontroli, text="Następna Tura", font=("Arial", 12, "bold"), command=self.wykonaj_ture).pack(
            side=tk.LEFT, padx=20)
        tk.Button(panel_kontroli, text="Zapisz Grę", command=lambda: print("Zapisywanie...")).pack(side=tk.LEFT, padx=5)
        tk.Button(panel_kontroli, text="Wczytaj Grę", command=lambda: print("Wczytywanie...")).pack(side=tk.LEFT,
                                                                                                    padx=5)

    def zbuduj_panel_logow(self):
        ramka_logow = tk.Frame(self.root)
        ramka_logow.pack(side=tk.RIGHT, fill=tk.Y)

        self.przestrzen_logow = tk.Text(ramka_logow, width=40, state=tk.DISABLED, bg="#f4f4f4")
        scrollbar = tk.Scrollbar(ramka_logow, command=self.przestrzen_logow.yview)
        self.przestrzen_logow.config(yscrollcommand=scrollbar.set)

        self.przestrzen_logow.pack(side=tk.LEFT, fill=tk.Y)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def wykonaj_ture(self):
        self.swiat.wykonaj_ture()
        self.panel_gry.odswiez()
        self.aktualizuj_logi()

    def aktualizuj_logi(self):
        self.przestrzen_logow.config(state=tk.NORMAL)
        self.przestrzen_logow.delete(1.0, tk.END)
        for log in self.swiat.get_logi():
            self.przestrzen_logow.insert(tk.END, log + "\n")
        self.przestrzen_logow.config(state=tk.DISABLED)
        self.przestrzen_logow.see(tk.END)  # Automatyczne przewijanie w dół


class PanelGry(tk.Canvas):
    def __init__(self, master, swiat, okno_glowne, **kwargs):
        super().__init__(master, bg="white", **kwargs)
        self.swiat = swiat
        self.okno_glowne = okno_glowne

        # Obsługa kliknięcia myszką do dodawania organizmów
        self.bind("<Button-1>", self.klikniecie_myszy)

        # Zmuszamy Canvas do przyjmowania wciśnięć klawiatury
        self.focus_set()

    def klikniecie_myszy(self, event):
        self.focus_set()  # Przywraca focus klawiatury na planszę po kliknięciu
        kafel = self.przelicz_piksele_na_wspolrzedne(event.x, event.y)

        if kafel is not None and self.swiat.get_organizm_na_polu(kafel[0], kafel[1]) is None:
            self.pokaz_menu(kafel[0], kafel[1], event.x_root, event.y_root)

    def pokaz_menu(self, x, y, ekran_x, ekran_y):
        menu = tk.Menu(self, tearoff=0)
        # Zakładam że RejestrGatunkow.get_nazwy_klas() zwraca słownik
        # np. {"Wilk": "sciezka.do.Wilk", "Owca": ...}
        moje_gatunki = RejestrGatunkow.get_nazwy_klas()

        for nazwa_gatunku, sciezka in moje_gatunki.items():
            if nazwa_gatunku == "Czlowiek" and self.swiat.get_czlowiek() is not None:
                continue

            # Używamy sztuczki 'n=nazwa_gatunku' aby zapamiętać wartość w lambdzie!
            menu.add_command(
                label=f"Dodaj {nazwa_gatunku}",
                command=lambda n=nazwa_gatunku: self.dodaj_organizm(n, x, y)
            )

        menu.post(ekran_x, ekran_y)

    def dodaj_organizm(self, nazwa, x, y):
        sciezka = RejestrGatunkow.get_nazwy_klas()[nazwa]
        self.swiat.stworz_i_dodaj_organizm(sciezka, x, y)
        self.odswiez()

    def przelicz_piksele_na_wspolrzedne(self, x, y):
        raise NotImplementedError

    def odswiez(self):
        raise NotImplementedError


class PanelGrySiatka(PanelGry):
    ROZMIAR_POLA = 30

    def __init__(self, master, swiat, okno_glowne):
        szerokosc = swiat.get_size_x() * self.ROZMIAR_POLA
        wysokosc = swiat.get_size_y() * self.ROZMIAR_POLA
        super().__init__(master, swiat, okno_glowne, width=szerokosc, height=wysokosc)

        self.bind("<KeyPress>", self.obsluga_klawiatury)

    def obsluga_klawiatury(self, event):
        gracz = self.swiat.get_czlowiek()
        if not gracz: return

        klawisz = event.keysym.lower()
        czy_wykonano_akcje = False

        mapa_kierunkow = {
            'q': (-1, -1), 'w': (0, -1), 'e': (1, -1),
            'a': (-1, 0), 'd': (1, 0),
            'z': (-1, 1), 'x': (0, 1), 'c': (1, 1)
        }

        if klawisz in mapa_kierunkow:
            dx, dy = mapa_kierunkow[klawisz]
            gracz.ustaw_kierunek_ruchu(dx, dy)
            czy_wykonano_akcje = True
        elif klawisz == 's':
            gracz.aktywuj_umiejetnosc()
            czy_wykonano_akcje = True

        if czy_wykonano_akcje:
            self.okno_glowne.wykonaj_ture()

    def przelicz_piksele_na_wspolrzedne(self, x, y):
        px = x // self.ROZMIAR_POLA
        py = y // self.ROZMIAR_POLA
        if 0 <= px < self.swiat.get_size_x() and 0 <= py < self.swiat.get_size_y():
            return (px, py)
        return None

    def odswiez(self):
        self.delete("all")  # Czyści całe płótno

        for x in range(self.swiat.get_size_x()):
            for y in range(self.swiat.get_size_y()):
                px = x * self.ROZMIAR_POLA
                py = y * self.ROZMIAR_POLA

                org = self.swiat.get_organizm_na_polu(x, y)
                if org:
                    # Rysujemy prostokąt w odpowiednim kolorze
                    self.create_rectangle(px, py, px + self.ROZMIAR_POLA, py + self.ROZMIAR_POLA, fill=org.get_kolor(),
                                          outline="black")
                    # W Tkinterze tekst sam idealnie się środkuje względem punktu!
                    self.create_text(px + self.ROZMIAR_POLA / 2, py + self.ROZMIAR_POLA / 2, text=org.get_znak(),
                                     fill="white", font=("Arial", 14, "bold"))
                else:
                    self.create_rectangle(px, py, px + self.ROZMIAR_POLA, py + self.ROZMIAR_POLA, fill="white",
                                          outline="lightgray")


class PanelGryHex(PanelGry):
    PROMIEN = 20
    WYSOKOSC = math.sqrt(3) * PROMIEN
    PRZESUNIECIE_X = 1.5 * PROMIEN

    def __init__(self, master, swiat, okno_glowne):
        szerokosc = int(swiat.get_size_x() * self.PRZESUNIECIE_X + (self.PROMIEN / 2.0))
        wysokosc = int(swiat.get_size_y() * self.WYSOKOSC + (self.WYSOKOSC / 2.0))
        super().__init__(master, swiat, okno_glowne, width=szerokosc, height=wysokosc)

        self.bind("<KeyPress>", self.obsluga_klawiatury)

    def obsluga_klawiatury(self, event):
        gracz = self.swiat.get_czlowiek()
        if not gracz: return

        x = gracz.x
        parzysta = (x % 2 == 0)
        klawisz = event.keysym.lower()
        czy_wykonano_akcje = False

        if klawisz == 'w':
            gracz.ustaw_kierunek_ruchu(0, -1)
            czy_wykonano_akcje = True
        elif klawisz == 's':
            gracz.ustaw_kierunek_ruchu(0, 1)
            czy_wykonano_akcje = True
        elif klawisz == 'q':
            gracz.ustaw_kierunek_ruchu(-1, -1 if parzysta else 0)
            czy_wykonano_akcje = True
        elif klawisz == 'a':
            gracz.ustaw_kierunek_ruchu(-1, 0 if parzysta else 1)
            czy_wykonano_akcje = True
        elif klawisz == 'e':
            gracz.ustaw_kierunek_ruchu(1, -1 if parzysta else 0)
            czy_wykonano_akcje = True
        elif klawisz == 'd':
            gracz.ustaw_kierunek_ruchu(1, 0 if parzysta else 1)
            czy_wykonano_akcje = True
        elif klawisz == 'space':
            gracz.aktywuj_umiejetnosc()
            czy_wykonano_akcje = True

        if czy_wykonano_akcje:
            self.okno_glowne.wykonaj_ture()

    def buduj_heksagon(self, cx, cy):
        # Tworzy listę koordynatów [x1, y1, x2, y2...] dla narysowania polygonu
        punkty = []
        for i in range(6):
            kat_rad = math.pi / 180 * (60 * i)
            px = cx + self.PROMIEN * math.cos(kat_rad)
            py = cy + self.PROMIEN * math.sin(kat_rad)
            punkty.extend([px, py])
        return punkty

    def wylicz_srodek(self, x, y):
        srodek_x = x * self.PRZESUNIECIE_X + self.PROMIEN
        srodek_y = y * self.WYSOKOSC + (self.WYSOKOSC / 2.0)
        if x % 2 != 0:
            srodek_y += (self.WYSOKOSC / 2.0)
        return srodek_x, srodek_y

    def przelicz_piksele_na_wspolrzedne(self, mysz_x, mysz_y):
        # Szybka i prosta detekcja kolizji (brute-force tak jak w Javie)
        # Przy małej mapie 20x20 działa wystarczająco szybko
        for x in range(self.swiat.get_size_x()):
            for y in range(self.swiat.get_size_y()):
                cx, cy = self.wylicz_srodek(x, y)
                # Oblicz dystans od środka hexu do myszki
                dystans = math.hypot(mysz_x - cx, mysz_y - cy)
                # Wymagany by kliknąć blisko środka (uproszczona matematyka kolizji koła wpisanego)
                if dystans < (self.WYSOKOSC / 2.0):
                    return (x, y)
        return None

    def odswiez(self):
        self.delete("all")

        for x in range(self.swiat.get_size_x()):
            for y in range(self.swiat.get_size_y()):
                cx, cy = self.wylicz_srodek(x, y)
                punkty_hex = self.buduj_heksagon(cx, cy)

                org = self.swiat.get_organizm_na_polu(x, y)
                if org:
                    self.create_polygon(punkty_hex, fill=org.get_kolor(), outline="black")
                    self.create_text(cx, cy, text=org.get_znak(), fill="white", font=("Arial", 12, "bold"))
                else:
                    self.create_polygon(punkty_hex, fill="white", outline="black")


# Aby uruchomić aplikację:
if __name__ == "__main__":
    root = tk.Tk()
    app = OknoPowitalne(root)
    root.mainloop()