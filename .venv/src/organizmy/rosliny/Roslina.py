import random
from swiat import Swiat
from Organizm import Organizm
from Zwierze import Zwierze

class Roslina(Organizm):
    SZANSA_NA_ROZSIEW = 10

    def __init__(self, swiat, x: int, y: int, sila: int):
        super().__init__(swiat, x, y, sila, 0)

    def akcja(self):
        self.wiek += 1
        if random.randint(0, 99) < self.SZANSA_NA_ROZSIEW:
            self.rozsiej()

    def kolizja(self, drugi: Organizm):
        if isinstance(drugi, Zwierze) and not drugi.czyJestDrapieznikiem():
            self.zabij()

    def rozsiej(self):
        opcje = self.swiat.getWolneSasiedniePola(self.x, self.y)

        if opcje:
            p = random.choice(opcje)
            potomek = self.stworzNowy(p.x, p.y)
            self.swiat.dodajNowyOrganizm(potomek)
            self.swiat.dodajLog(f"Wyrosła nowa roślina: {potomek.getNazwa()}")

