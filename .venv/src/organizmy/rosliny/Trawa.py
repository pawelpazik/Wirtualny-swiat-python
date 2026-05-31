from src.organizmy.rosliny.Roslina import Roslina
from src.organizmy.Organizm import Organizm

class Trawa(Roslina):

    def __init__(self, swiat, x: int, y: int, sila: int = 0, wiek: int = 0):
        super().__init__(swiat, x, y, sila)
        self.wiek = wiek

    def stworz_nowy(self, x: int, y: int) -> Organizm:
        return Trawa(self.swiat, x, y)

    def get_nazwa(self) -> str:
        return "Trawa"

    def get_znak(self) -> str:
        return 'T'

    def get_kolor(self) -> str:
        return "#267d26"
