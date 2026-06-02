import random
from src.organizmy.Organizm import Organizm

class Zwierze(Organizm):
    def __init__(self, swiat: 'Swiat', x: int, y: int, sila: int, inicjatywa: int):
        super().__init__(swiat, x, y, sila, inicjatywa)
        self.p_x = x
        self.p_y = y

    def akcja(self):
        self.wiek += 1
        self.p_x = self.x
        self.p_y = self.y

        mozliwosci = self.swiat.get_sasiednie_pola(self.x, self.y)

        if len(mozliwosci) > 0:
            nowe_pole = random.choice(mozliwosci)
            self.swiat.przesun_na_planszy(self, nowe_pole.x, nowe_pole.y)

    def kolizja(self, drugi: 'Organizm'):
        if drugi is None:
            return

        from src.organizmy.rosliny.Roslina import Roslina

        if type(self) == type(drugi):
            self.wroc_na_pozycje()
            self.swiat.przywroc_na_plansze(drugi)
            if self.wiek > 3 and drugi.get_wiek() > 3:
                self.rozmnoz()
            return

        if isinstance(drugi, Roslina):
            drugi.kolizja(self)
            if self.czy_zyje():
                if not self.czy_jest_drapieznikiem():
                    drugi.zabij()
                    self.swiat.usun_z_planszy(drugi)
                    self.swiat.dodaj_log(f"{self.get_nazwa()} zjada {drugi.get_nazwa()}")
                else:
                    pass
            return

        if drugi.czy_odbil_atak(self):
            self.swiat.dodaj_log(f"{drugi.get_nazwa()} odbił atak {self.get_nazwa()}")
            self.wroc_na_pozycje()
            self.swiat.przywroc_na_plansze(drugi)
            return

        if self.czy_ucieka():
            self.przesun_na_puste()
            self.swiat.dodaj_log(f"{self.get_nazwa()} ucieka przed {drugi.get_nazwa()}")
            self.swiat.przywroc_na_plansze(drugi)
            return

        if drugi.czy_ucieka():
            drugi.przesun_na_puste()
            self.swiat.dodaj_log(f"{drugi.get_nazwa()} ucieka przed {self.get_nazwa()}")
            return

        if self.get_sila() >= drugi.get_sila():
            drugi.zabij()
            self.swiat.usun_z_planszy(drugi)
            self.swiat.dodaj_log(f"{self.get_nazwa()} zjada {drugi.get_nazwa()}")
        else:
            self.zabij()
            self.swiat.usun_z_planszy(self)
            self.swiat.przywroc_na_plansze(drugi)
            self.swiat.dodaj_log(f"{drugi.get_nazwa()} pokonuje {self.get_nazwa()}")

    def rozmnoz(self):
        opcje = self.swiat.get_wolne_sasiednie_pola(self.x, self.y)
        if opcje:
            p = random.choice(opcje)
            potomek = self.stworz_nowy(p.x, p.y)
            self.swiat.dodaj_nowy_organizm(potomek)
            self.swiat.dodaj_log(f"Urodził się nowy gatunek: {potomek.get_nazwa()}")

    def wroc_na_pozycje(self):
        self.swiat.przesun_na_planszy(self, self.p_x, self.p_y)

    def przesun_na_puste(self):
        opcje = self.swiat.get_wolne_sasiednie_pola(self.x, self.y)
        if opcje:
            p = random.choice(opcje)
            self.swiat.przesun_na_planszy(self, p.x, p.y)

    def przesun_na_losowe(self):
        opcje = self.swiat.get_sasiednie_pola(self.x, self.y)
        if opcje:
            p = random.choice(opcje)
            self.swiat.przesun_na_planszy(self, p.x, p.y)

    def czy_odporny_na_barszcz(self) -> bool:
        return False

    def czy_jest_drapieznikiem(self) -> bool:
        return False