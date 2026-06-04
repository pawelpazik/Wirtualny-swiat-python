from src.organizmy.rosliny.Roslina import Roslina
from src.organizmy.Organizm import Organizm
from src.organizmy.zwierzeta.Zwierze import Zwierze


class WilczeJagody(Roslina):

    def __init__(self, swiat, x: int, y: int, sila: int = 99, wiek: int = 0):
        super().__init__(swiat, x, y, sila)
        self.wiek = wiek

    def kolizja(self, drugi: Organizm):
        if isinstance(drugi, Zwierze) and drugi.czy_zyje():
            drugi.zabij()
            self.zabij()
            self.swiat.dodaj_log(drugi.get_nazwa() + " zjadl wilcze jaogdy i umiera.")

    def stworz_nowy(self, x: int, y: int) -> Organizm:
        return WilczeJagody(self.swiat, x, y)

    def get_nazwa(self) -> str:
        return "Wilcze Jagody"

    def get_znak(self) -> str:
        return 'J'

    def get_kolor(self) -> str:
        return "#267d26"
