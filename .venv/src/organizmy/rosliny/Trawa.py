class Trawa(Roslina):

    def __init__(self, swiat, x: int, y: int):
        super().__init__(swiat, x, y, 0, 0)

    def __init__(self, swiat, x: int, y: int, sila: int, wiek: int):
        super().__init__(swiat, x, y, sila, 0)
        self.wiek = wiek

    def stworzNowy(self, x: int, y: int) -> Organizm:
        return Trawa(self.swiat, x, y)

    def getNazwa(self) -> str:
        return "Trawa"

    def getZnak(self) -> str:
        return 'T'

    def getKolor(self) -> str:
        return "#267d26"
