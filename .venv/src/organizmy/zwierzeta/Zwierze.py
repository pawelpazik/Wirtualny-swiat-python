from organizmy import Organizm
from swiat import Swiat


class Zwierze:
    def __init__(self, swiat, x, y, sila, inicjatywa):
        super().__init__(x, y, sila, inicjatywa)
        this.pX = x
        this.pY = y

    def akcja(self):
        self.wiek+=1
        this.pX = this.x
        this.pY = this.y

        mozliwosci = swiat.getSasiedniePola(this.x, this.y)

        if mozliwosci.len() != 0:
            nowePole = mozliwosci.get(random.nextInt(mozliwosci.size()))
            this.x = nowePole.x
            this.y = nowePole.y

    def kolizja(self, organizmDrugi):
        from Roslina import Roslina

        if type(self) == type(organizmDrugi):
            self.wrocNaPozycje()
            if self.wiek > 3 and drugi.get_wiek() > 3:
                self.rozmnoz()
            elif isinstance(drugi, Roslina):
                drugi.kolizja(self)
            else:
                if drugi.czy_odbil_atak(self):
                    self.swiat.dodaj_log(f"{drugi.get_nazwa()} odbił atak {self.get_nazwa()}")
                    self.wroc_na_pozycje()
                elif self.czy_ucieka():
                    self.przesun_na_puste()
                    self.swiat.dodaj_log(f"{self.get_nazwa()} ucieka przed {drugi.get_nazwa()}")
                elif drugi.czy_ucieka():
                    drugi.przesun_na_puste()
                    self.swiat.dodaj_log(f"{drugi.get_nazwa()} ucieka przed {self.get_nazwa()}")
                elif self.get_sila() >= drugi.get_sila():
                    drugi.zabij()
                    self.swiat.dodaj_log(f"{self.get_nazwa()} zjada {drugi.get_nazwa()}")
                else:
                    self.zabij()
                    self.swiat.dodaj_log(f"{drugi.get_nazwa()} pokonuje {self.get_nazwa()}")

    def rozmnoz(self):
        opcje = self.swiat.getWolneSasiedniePola(self.x, self.y)
        if opcje:
            p = random.choice(opcje)
            potomek = self.stworz_nowy(p.x, p.y)
            self.swiat.dodaj_nowy_organizm(potomek)
            self.swiat.dodaj_log(f"Urodził się nowy {potomek.get_nazwa()}")

    def wrocNaPozycje(self):
        self.x = self.pX
        self.y = self.pY

    def przesunNaPuste(self):
        opcje = self.swiat.getWolneSasiedniePola(self.x, self.y)
        if opcje:
            p = random.choice(opcje)
            self.x = p.x
            self.y = p.y

    def przesunNaLosowe(self):
        opcje = self.swiat.getSasiedniePola(self.x, self.y)
        if opcje:
            p = random.choice(opcje)
            self.x = p.x
            self.y = p.y

    def czyOdpornyNaBarszcz(self) -> bool:
        return False

    def czyJestDrapieznikiem(self) -> bool:
        return False