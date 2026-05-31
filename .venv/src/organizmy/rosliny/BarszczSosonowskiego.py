from src.organizmy.rosliny.Roslina import Roslina
from src.organizmy.Organizm import Organizm
from src.organizmy.zwierzeta.Zwierze import Zwierze


class BarszczSosnowskiego(Roslina):

    def __init__(self, swiat, x: int, y: int, sila: int = 10, wiek: int = 0):
        super().__init__(swiat, x, y, sila)
        self.wiek = wiek


    def akcja(self):
        self.wiek += 1
        polaWokol = self.swiat.get_sasiednie_pola(self.x, self.y)
        for p in polaWokol:
            xO = p.x
            yO = p.y
            ofiara = self.swiat.get_organizm_na_polu(xO, yO)
            if (isinstance(ofiara, Zwierze)) and ofiara.czy_zyje():
                if not ofiara.czy_odporny_na_barszcz():
                    ofiara.zabij()
                    self.swiat.dodaj_log(self.get_nazwa() + "zabija zwierze w poblizu: " + ofiara.get_nazwa())

    def kolizja(self, drugi: Organizm):
        if isinstance(drugi, Zwierze):
            if drugi.czy_zyje():
                drugi.przesun_na_puste()
                self.swiat.dodaj_log(drugi.get_nazwa() + "ucieka przed: " + self.get_nazwa())
                return
            if not drugi.czy_odporny_na_barszcz():
                drugi.zabij()
                self.swiat.dodaj_log(drugi.get_nazwa() + " zjadl " + self.get_nazwa() + " i umiera");
                return

            self.swiat.dodaj_log(napastnik.get_nazwa() + " zjadl " + self.get_nazwa());
            self.zabij();

    def stworz_nowy(self, x: int, y: int) -> Organizm:
        return BarszczSosnowskiego(self.swiat, x, y)

    def get_nazwa(self) -> str:
        return "Barszcz Sosnowskiego"

    def get_znak(self) -> str:
        return 'B'

    def get_kolor(self) -> str:
        return "#d8ffbf"
