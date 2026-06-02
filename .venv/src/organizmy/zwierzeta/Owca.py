from src.organizmy.zwierzeta.Zwierze import Zwierze
from src.organizmy.Organizm import Organizm

class Owca(Zwierze):

    def __init__(self, swiat, x: int, y: int, sila: int = 4, wiek: int = 0):
        super().__init__(swiat, x, y, sila, 4)
        self.wiek = wiek

    def czy_jest_drapieznikiem(self) -> bool:
        return False

    def stworz_nowy(self, x: int, y: int) -> Organizm:
        return Owca(self.swiat, x, y)


    def get_nazwa(self) -> str:
        return "Owca"


    def get_znak(self) -> str:
        return 'O'


    def get_kolor(self) -> str:
        return "#bdbdbd"