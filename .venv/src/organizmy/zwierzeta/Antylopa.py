from src.organizmy.zwierzeta.Zwierze import Zwierze
from src.organizmy.Organizm import Organizm
import random

class Antylopa(Zwierze):

    def __init__(self, swiat, x: int, y: int, sila: int = 4, wiek: int = 0):
        super().__init__(swiat, x, y, sila, 4)
        self.wiek = wiek

    def akcja(self):
        self.wiek+=1

        self.px = self.x
        self.py = self.y

        opcje_zasieg_1 = self.swiat.get_sasiednie_pola(self.x, self.y)
        wszystkie_opcje = []

        for p1 in opcje_zasieg_1:
            wszystkie_opcje.append(p1)
            opcje_zasieg_2 = self.swiat.get_sasiednie_pola(p1.x, p1.y)
            for p2 in opcje_zasieg_2:
                wszystkie_opcje.append(p2)

        unikalne_opcje = list({(p.x, p.y): p for p in wszystkie_opcje}.values())

        if unikalne_opcje:
            nowe_pole = random.choice(unikalne_opcje)
            print(f"DEBUG: Antylopa przeskoczyła z ({self.x}, {self.y}) na ({nowe_pole.x}, {nowe_pole.y})")
            self.swiat.przesun_na_planszy(self, nowe_pole.x, nowe_pole.y)


    def czy_ucieka(self) -> bool:
        if random.randint(0, 1) == 0:
            return True

    def czy_jest_drapieznikiem(self) -> bool:
        return False

    def stworz_nowy(self, x: int, y: int) -> Organizm:
        return Antylopa(self.swiat, x, y)

    def get_nazwa(self) -> str:
        return "Antylopa"


    def get_znak(self) -> str:
        return 'A'


    def get_kolor(self) -> str:
        return "#cc6666"