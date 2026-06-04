from src.organizmy.rosliny.BarszczSosonowskiego import BarszczSosnowskiego
from src.organizmy.zwierzeta.Zwierze import Zwierze
from src.organizmy.Organizm import Organizm
import math

class CyberOwca(Zwierze):

    def __init__(self, swiat, x: int, y: int, sila: int = 10, wiek: int = 0):
        super().__init__(swiat, x, y, sila, 4)
        self.wiek = wiek

    def akcja(self):
        najblizszy_barszcz = None
        najmniejsza_odleglosc = math.inf

        for o in self.swiat.get_organizmy():
            if isinstance(o, BarszczSosnowskiego):
                dx = o.get_x()
                dy = o.get_y()
                odleglosc = math.sqrt(dx * dx + dy * dy)
                if odleglosc < najmniejsza_odleglosc:
                    najmniejsza_odleglosc = odleglosc
                    najblizszy_barszcz = o
        if najblizszy_barszcz != None:
            self.wiek += 1
            najlepsze_pole = None
            najmniejsza_odleglosc = math.inf

            for p in self.swiat.get_sasiednie_pola(self.x, self.y):
                dx = najblizszy_barszcz.get_x() - p.x
                dy = najblizszy_barszcz.get_y() - p.y
                odleglosc = math.sqrt(dx * dx + dy * dy)
                if odleglosc < najmniejsza_odleglosc:
                    najmniejsza_odleglosc = odleglosc
                    najlepsze_pole = p

            if najlepsze_pole != None:
                self.p_x = self.x
                self.p_y = self.y
                self.swiat.przesun_na_planszy(self, najlepsze_pole.x, najlepsze_pole.y)
        else:
            super().akcja()

    def czy_jest_drapieznikiem(self) -> bool:
        return False

    def czy_odporny_na_barszcz(self) -> bool:
        return True

    def stworz_nowy(self, x: int, y: int) -> Organizm:
        return CyberOwca(self.swiat, x, y)


    def get_nazwa(self) -> str:
        return "Cyber Owca"


    def get_znak(self) -> str:
        return 'C'


    def get_kolor(self) -> str:
        return "#bdbdbd"