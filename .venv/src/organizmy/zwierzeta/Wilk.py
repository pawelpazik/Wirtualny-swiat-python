from src.organizmy.Organizm import Organizm
from src.organizmy.zwierzeta.Zwierze import Zwierze

class Wilk(Zwierze):

    def __init__(self, swiat, x: int, y: int, sila: int = 9, wiek: int = 5):
        super().__init__(swiat, x, y, sila, 5)
        self.wiek = wiek

    def czy_jest_drapieznikiem(self) -> bool:
        return True

    def stworz_nowy(self, x: int, y: int) -> Organizm:
        return Wilk(self.swiat, x, y)


    def get_nazwa(self) -> str:
        return "Wilk"


    def get_znak(self) -> str:
        return 'W'


    def get_kolor(self) -> str:
        return "#8c8180"