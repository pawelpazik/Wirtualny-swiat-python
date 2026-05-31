from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

# Import potrzebny TYLKO do podpowiadania kodu (unika pętli)
if TYPE_CHECKING:
    from src.swiat.Swiat import Swiat

class Organizm(ABC):
    def __init__(self, swiat: 'Swiat', x: int, y: int, sila: int, inicjatywa: int):
        self.swiat = swiat
        self.x = x
        self.y = y
        self.sila = sila
        self.inicjatywa = inicjatywa
        self.wiek = 0
        self.zyje = True

    @abstractmethod
    def akcja(self):
        pass

    @abstractmethod
    def kolizja(self, organizm_drugi: 'Organizm'):
        pass

    @abstractmethod
    def get_nazwa(self) -> str:
        pass

    @abstractmethod
    def stworz_nowy(self, x: int, y: int) -> 'Organizm':
        pass

    def czy_ucieka(self) -> bool:
        return False

    def czy_odbil_atak(self, napastnik: 'Organizm') -> bool:
        return False

    def get_sila(self) -> int:
        return self.sila

    def set_sila(self, sila: int):
        self.sila = sila

    def get_inicjatywa(self) -> int:
        return self.inicjatywa

    def get_x(self) -> int:
        return self.x

    def get_y(self) -> int:
        return self.y

    def get_wiek(self) -> int:
        return self.wiek

    def czy_zyje(self) -> bool:
        return self.zyje

    def zabij(self):
        self.zyje = False
        self.swiat.usun_z_planszy(self)

    @abstractmethod
    def get_znak(self) -> str:
        pass

    @abstractmethod
    def get_kolor(self) -> str:
        pass