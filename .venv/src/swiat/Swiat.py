import sys
import random
import importlib
from abc import ABC, abstractmethod
from typing import List, Optional, TYPE_CHECKING
from src.swiat.Punkt import Punkt

if TYPE_CHECKING:
    from src.organizmy.Organizm import Organizm

class Swiat(ABC):
    def __init__(self, size_x: int, size_y: int):
        self.size_x = size_x
        self.size_y = size_y
        self.organizmy = []
        self.noworodki = []
        self.logi = []
        self.warstwy = 2
        self.generowanie = True

        self.plansza = [
            [
                [None for _ in range(self.warstwy)]
                for _ in range(self.size_y)
            ]
            for _ in range(self.size_x)
        ]

    @abstractmethod
    def get_sasiednie_pola(self, x: int, y: int) -> List[Punkt]:
        pass

    @abstractmethod
    def czy_hex(self) -> bool:
        pass

    def get_wolne_sasiednie_pola(self, x: int, y: int) -> List[Punkt]:
        wolne = []
        for p in self.get_sasiednie_pola(x, y):
            if self.get_organizm_na_polu(p.x, p.y) is None:
                wolne.append(p)
        return wolne

    def get_bezpieczne_sasiednie_pola(self, x: int, y: int, sila: int) -> List[Punkt]:
        bezpieczne = []
        for p in self.get_sasiednie_pola(x, y):
            org = self.get_organizm_na_polu(p.x, p.y)
            if org is None or org.get_sila() < sila:
                bezpieczne.append(p)
        return bezpieczne

    def get_czlowiek(self) -> Optional['Organizm']:
        for o in self.organizmy:
            if type(o).__name__ == 'Czlowiek' and o.czy_zyje():
                return o
        return None

    def wykonaj_ture(self):
        self.generowanie = False
        self.logi.clear()
        self.organizmy.sort(key=lambda o: (o.get_inicjatywa(), o.get_wiek()), reverse=True)

        for i in range(len(self.organizmy)):
            o = self.organizmy[i]
            if o.czy_zyje():
                o.akcja()
                self.obsluz_kolizje(o)

        # Pythonowe czyszczenie list
        self.organizmy = [o for o in self.organizmy if o.czy_zyje()]
        self.organizmy.extend(self.noworodki)
        self.noworodki.clear()

    def obsluz_kolizje(self, o: 'Organizm'):
        for inny in self.organizmy:
            if (inny != o and inny.czy_zyje() and o.czy_zyje() and
                    inny.get_x() == o.get_x() and inny.get_y() == o.get_y()):
                o.kolizja(inny)

    def dodaj_nowy_organizm(self, organizm: 'Organizm'):
        from src.organizmy.rosliny.Roslina import Roslina

        if isinstance(organizm, Roslina):
            warstwa = 0
        else:
            warstwa = 1

        self.plansza[organizm.x][organizm.y][warstwa] = organizm

        if self.generowanie:
            self.organizmy.append(organizm)
        else:
            self.noworodki.append(organizm)

    def przesun_na_planszy(self, organizm: 'Organizm', nowy_x: int, nowy_y: int):
        from src.organizmy.rosliny.Roslina import Roslina
        warstwa = 0 if isinstance(organizm, Roslina) else 1

        self.plansza[organizm.x][organizm.y][warstwa] = None
        organizm.x = nowy_x
        organizm.y = nowy_y
        self.plansza[nowy_x][nowy_y][warstwa] = organizm

    def usun_z_planszy(self, organizm: 'Organizm'):
        from src.organizmy.rosliny.Roslina import Roslina

        warstwa = 0 if isinstance(organizm, Roslina) else 1

        if self.plansza[organizm.x][organizm.y][warstwa] == organizm:
            self.plansza[organizm.x][organizm.y][warstwa] = None

    def get_organizm_na_polu(self, x: int, y: int) -> Optional['Organizm']:
        zwierze = self.plansza[x][y][1]
        if zwierze is not None:
            return zwierze

        roslina = self.plansza[x][y][0]
        if roslina is not None:
            return roslina

        return None

    def get_konstruktor(self, nazwa_gatunku: str, x: int, y: int):
        try:
            modul_nazwa, klasa_nazwa = nazwa_gatunku.rsplit('.', 1)
            modul = importlib.import_module(modul_nazwa)
            klasa = getattr(modul, klasa_nazwa)
            return klasa(self, x, y)
        except Exception as e:
            print(f"Błąd podczas tworzenia: {nazwa_gatunku}", file=sys.stderr)
            print(e, file=sys.stderr)
            return None

    def stworz_i_dodaj_organizm(self, nazwa_gatunku: str, x: int, y: int):
        nowy = self.get_konstruktor(nazwa_gatunku, x, y)
        if nowy is not None:
            self.dodaj_nowy_organizm(nowy)

    def dodaj_log(self, log: str):
        self.logi.append(log)

    def get_konstruktor_do_odczytu(self, nazwa_gatunku: str, x: int, y: int, sila: float, wiek: int):
        from src.utils.RejestrGatunkow import RejestrGatunkow

        sciezka_do_klasy = RejestrGatunkow.get_nazwy_klas().get(nazwa_gatunku)

        if sciezka_do_klasy is None:
            print(f"Nieznany gatunek w pliku konfiguracyjnym: {nazwa_gatunku}", file=sys.stderr)
            return None

        try:
            modul_nazwa, klasa_nazwa = sciezka_do_klasy.rsplit('.', 1)
            modul = importlib.import_module(modul_nazwa)
            klasa = getattr(modul, klasa_nazwa)
            return klasa(self, x, y, sila, wiek)
        except Exception as e:
            print(f"Błąd podczas odtwarzania z pliku: {nazwa_gatunku}", file=sys.stderr)
            print(e, file=sys.stderr)
            return None

    def generuj_plansze(self):
        from src.utils.RejestrGatunkow import RejestrGatunkow
        from src.organizmy.zwierzeta.Czlowiek import Czlowiek

        liczba_pol = self.size_x * self.size_y
        docelowa_liczba_organizmow = int(liczba_pol * 0.15)

        dostepne_gatunki = list(RejestrGatunkow.get_nazwy_klas().keys())
        if "Czlowiek" in dostepne_gatunki:
            dostepne_gatunki.remove("Czlowiek")

        if not dostepne_gatunki:
            print("Błąd generowania: Rejestr gatunków jest pusty!", file=sys.stderr)
            return

        dodano_gracza = False
        while not dodano_gracza:
            cx = random.randint(0, self.size_x - 1)
            cy = random.randint(0, self.size_y - 1)
            if self.get_organizm_na_polu(cx, cy) is None:
                self.dodaj_nowy_organizm(Czlowiek(self, cx, cy))
                dodano_gracza = True

        udane_dodania = 0
        licznik_bezpieczenstwa = 0

        while udane_dodania < docelowa_liczba_organizmow and licznik_bezpieczenstwa < 2000:
            licznik_bezpieczenstwa += 1

            x = random.randint(0, self.size_x - 1)
            y = random.randint(0, self.size_y - 1)

            if self.get_organizm_na_polu(x, y) is None:
                wylosowany_gatunek = random.choice(dostepne_gatunki)
                sciezka_do_klasy = RejestrGatunkow.get_nazwy_klas().get(wylosowany_gatunek)

                self.stworz_i_dodaj_organizm(sciezka_do_klasy, x, y)
                udane_dodania += 1

        print(f"Pomyślnie wygenerowano nowy świat. Dodano gracza oraz {udane_dodania} organizmów.")

    def get_size_x(self):
        return self.size_x

    def get_size_y(self):
        return self.size_y

    def set_size_x(self, size_x: int):
        self.size_x = size_x

    def set_size_y(self, size_y: int):
        self.size_y = size_y

    def get_organizmy(self):
        return self.organizmy

    def get_noworodki(self):
        return self.noworodki

    def get_logi(self):
        return self.logi