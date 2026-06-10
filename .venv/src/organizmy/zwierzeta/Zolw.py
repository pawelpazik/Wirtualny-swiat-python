from src.organizmy.zwierzeta.Zwierze import Zwierze
from src.organizmy.Organizm import Organizm
import random

class Zolw(Zwierze):

    def __init__(self, swiat, x: int, y: int, sila: int = 2, wiek: int = 0):
        super().__init__(swiat, x, y, sila, 1)
        self.wiek = wiek

    def akcja(self):
        self.wiek += 1
        if random.randint(0, 3) == 0:
            self.p_x = self.x
            self.p_y = self.y

            mozliwosci = self.swiat.get_sasiednie_pola(self.p_x, self.p_y)

            if len(mozliwosci) > 0:
                nowe_pole = random.choice(mozliwosci)
                self.swiat.przesun_na_planszy(self, nowe_pole.x, nowe_pole.y)

    def czy_odbil_atak(self, napastnik: 'Organizm') -> bool:
        if napastnik.get_sila() < 5:
            return True

    def czy_jest_drapieznikiem(self) -> bool:
        return False

    def stworz_nowy(self, x: int, y: int) -> Organizm:
        return Zolw(self.swiat, x, y)


    def get_nazwa(self) -> str:
        return "Zolw"


    def get_znak(self) -> str:
        return 'Z'


    def get_kolor(self) -> str:
        return "#4d6600"