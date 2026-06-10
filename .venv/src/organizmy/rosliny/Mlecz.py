from src.organizmy.rosliny.Roslina import Roslina
from src.organizmy.Organizm import Organizm
import random

class Mlecz(Roslina):
    SZANSA_NA_ROZSIEW = 10

    def __init__(self, swiat, x: int, y: int, sila: int = 0, wiek: int = 0):
        super().__init__(swiat, x, y, sila)
        self.wiek = wiek

    def akcja(self):
        self.wiek += 1
        for i in range(3):
            if random.randint(0, 99) < self.SZANSA_NA_ROZSIEW:
                self.rozsiej()

    def stworz_nowy(self, x: int, y: int) -> Organizm:
        return Mlecz(self.swiat, x, y)

    def get_nazwa(self) -> str:
        return "Mlecz"

    def get_znak(self) -> str:
        return 'M'

    def get_kolor(self) -> str:
        return "#ffff00"
