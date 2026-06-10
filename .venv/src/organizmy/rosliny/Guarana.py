from src.organizmy.rosliny.Roslina import Roslina
from src.organizmy.Organizm import Organizm

class Guarana(Roslina):

    def __init__(self, swiat, x: int, y: int, sila: int = 0, wiek: int = 0):
        super().__init__(swiat, x, y, sila)
        self.wiek = wiek

    def kolizja(self, drugi: Organizm):
        drugi.set_sila(drugi.get_sila() + 3)
        self.zabij()
        self.swiat.dodaj_log(drugi.get_nazwa() + " zjada guarane i wzmacnia sile.")

    def stworz_nowy(self, x: int, y: int) -> Organizm:
        return Guarana(self.swiat, x, y)

    def get_nazwa(self) -> str:
        return "Guarana"

    def get_znak(self) -> str:
        return 'G'

    def get_kolor(self) -> str:
        return "#ff3333"
