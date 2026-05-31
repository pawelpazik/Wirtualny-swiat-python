import random
from src.organizmy.Organizm import Organizm
from src.organizmy.zwierzeta.Zwierze import Zwierze

class Roslina(Organizm):
    SZANSA_NA_ROZSIEW = 10

    def __init__(self, swiat, x: int, y: int, sila: int):
        super().__init__(swiat, x, y, sila, 0)

    def akcja(self):
        self.wiek += 1
        if random.randint(0, 99) < self.SZANSA_NA_ROZSIEW:
            self.rozsiej()

    def kolizja(self, drugi: Organizm):
        if isinstance(drugi, Zwierze):
            if not drugi.czy_jest_drapieznikiem:
                self.zabij()

    def rozsiej(self):
        opcje = self.swiat.get_wolne_sasiednie_pola(self.x, self.y)

        if opcje:
            p = random.choice(opcje)
            potomek = self.stworz_nowy(p.x, p.y)
            self.swiat.dodaj_nowy_organizm(potomek)
            self.swiat.dodaj_log(f"Wyrosła nowa roślina: {potomek.get_nazwa()}")

