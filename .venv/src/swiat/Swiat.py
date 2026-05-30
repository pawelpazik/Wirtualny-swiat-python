from abc import ABC, abstractmethod
from src.swiat.Punkt import Punkt
from src.organizmy.Organizm import Organizm
from src.swiat.SwiatSiatka import SwiatSiatka
from src.swiat.SwiatHex import SwiatHex


class Swiat(ABC):
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.organizmy = []
        self.noworodki = []
        self.logi = []
        self.warstwy = 2

        self.plansza = [
            [
                [None for _ in range(self.warstwy)]
                for _ in range(self.sizeY)
            ]
            for _ in range(self.sizeX)
        ]

    @abstractmethod
    def getSasiedniePola(self) -> List[Point]:
        pass

    @abstractmethod
    def czyHex(self) -> bool:
        pass

    def getWolneSasiedniePola(self, x ,y):
        wolne = [];
        for p in self.getSasiedniePola(x, y):
            if self.get_organizm_na_polu(p.x, p.y) is None:
                wolne.append(p)
        return wolne

    def getBezpieczneSasiedniePola(self, x, y, sila) -> List[Punkt]:
        bezpieczne = []
        for p in self.getSasiedniePola(self, x, y):
            org = self.get_organizm_na_polu(p.x, p.y)
            if org is None or org.getSila() < sila:
                bezpieczne.append(p)
        return bezpieczne

    def getCzlowiek(self):
        for o in self.organizmy:
            if type(o).__name__ == 'Czlowiek' and o.czyZyje():
                return o
        return None

    def wykonajTure(self):
        self.generowanie = False
        self.logi.clear()
        self.organizmy.sort(key=lambda o: (o.get_inicjatywa(), o.get_wiek()), reverse=True)

        for i in range(len(self.organizmy)):
            o = self.organizmy[i]
            if o.czy_zyje():
                o.akcja()
                self.obsluz_kolizje(o)

            self.organizmy = [o for o in self.organizmy if o.czy_zyje()]
            self.organizmy.extend(self.noworodki)
            self.noworodki.clear()

    def obsluzKolizje(self, o: Organizm):
        for inny in self.organizmy:
            if (inny != o and inny.czy_zyje() and o.czy_zyje() and
                    inny.get_x() == o.get_x() and inny.get_y() == o.get_y()):
                o.kolizja(inny)

    def dodajNowyOrgnanim(self, o: Organizm):
        if organizm.czy_jest_roslina():
            warstwa = 0
        else:
            warstwa = 1

        self.plansza[organizm.x][organizm.y][warstwa] = organizm

        if self.generowanie:
            self.organizmy.append(organizm)
        else:
            self.noworodki.append(organizm)

    def przesunNaPlanszy(self, organizm, nowy_x, nowy_y):
        warstwa = 0 if type(organizm) == Roslina else 1

        self.plansza[organizm.x][organizm.y][warstwa] = None

        organizm.x = nowy_x
        organizm.y = nowy_y

        self.plansza[nowy_x][nowy_y][warstwa] = organizm

    def getOrganizmNaPolu(self, x, y):
        zwierze = self.plansza[x][y][1]
        if zwierze is not None:
            return zwierze

        roslina = self.plansza[x][y][0]
        if roslina is not None:
            return roslina

        return None

    def getKonstruktor(self, nazwa_gatunku: str, x: int, y: int):
        try:
            modul_nazwa, klasa_nazwa = nazwa_gatunku.rsplit('.', 1)
            modul = importlib.import_module(modul_nazwa)
            klasa = getattr(modul, klasa_nazwa)
            return klasa(self, x, y)
        except Exception as e:
            print(f"Błąd podczas tworzenia: {nazwa_gatunku}", file=sys.stderr)
            print(e, file=sys.stderr)
            return None

    def stworzIDodajOrganizm(self, nazwa_gatunku: str, x: int, y: int):
        nowy = self.StworzOrganizm(nazwa_gatunku, x, y)
        if nowy is not None:
            self.dodajNowyOrgnanim(nowy)

    def dodajLog(self, log: str):
        self.logi.append(log)

    def getKonstruktorDoOdczytu(self, nazwa_gatunku: str, x: int, y: int, sila: float, wiek: int):
        from wirtualnySwiat.utils.RejestrGatunkow import RejestrGatunkow

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

    def generujPlansze(self):
        from wirtualnySwiat.utils.RejestrGatunkow import RejestrGatunkow
        from wirtualnySwiat.organizmy.zwierzeta.Czlowiek import Czlowiek

        liczba_pol = self.size_x * self.size_y
        docelowa_liczba_organizmow = int(liczba_pol * 0.15)

        dostepne_gatunki = list(RejestrGatunkow.get_nazwy_klas().keys())
        if "Czlowiek" in dostepne_gatunki:
            dostepne_gatunki.remove("Czlowiek")

        if not dostepne_gatunki:
            print("Błąd generowania: Rejestr gatunków jest pusty! Sprawdź plik konfiguracyjny.", file=sys.stderr)
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

        print(f"Pomyślnie wygenerowano nowy świat. Dodano gracza oraz {udane_dodania} losowych organizmów.")

    def getSizeX(self):
        return self.size_x

    def getSizeY(self):
        return self.size_y

    def setSizeX(self, size_x):
        self.size_x = size_x

    def setSizeY(self, size_y):
        self.size_y = size_y

    def getOrganizmy(self):
        return self.organizmy

    def getNoworodki(self):
        return self.noworodki

    def getLogi(self):
        return self.logi
