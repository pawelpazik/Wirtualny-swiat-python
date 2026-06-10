from src.organizmy.zwierzeta.Zwierze import Zwierze
from src.organizmy.Organizm import Organizm
import random

class Lis(Zwierze):

    def __init__(self, swiat, x: int, y: int, sila: int = 3, wiek: int = 0):
        super().__init__(swiat, x, y, sila, 7)
        self.wiek = wiek

    def akcja(self):
        self.wiek += 1
        self.p_x = self.x
        self.p_y = self.y

        mozliwosci = self.swiat.get_bezpieczne_sasiednie_pola(self.p_x, self.p_y, self.sila)

        if len(mozliwosci) > 0:
            nowe_pole = random.choice(mozliwosci)
            self.swiat.przesun_na_planszy(self, nowe_pole.x, nowe_pole.y)


    def czy_jest_drapieznikiem(self) -> bool:
        return True

    def stworz_nowy(self, x: int, y: int) -> Organizm:
        return Lis(self.swiat, x, y)


    def get_nazwa(self) -> str:
        return "Lis"


    def get_znak(self) -> str:
        return 'L'


    def get_kolor(self) -> str:
        return "#ff9900"