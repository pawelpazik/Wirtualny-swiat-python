from src.swiat.Swiat import Swiat
from src.swiat.Punkt import Punkt

class SwiatHex(Swiat):
    def __init__(self, size_x: int, size_y: int):
        super().__init__(size_x, size_y)

    def czy_hex(self) -> bool:
        return True

    def get_sasiednie_pola(self, x: int, y: int):
        sasiedzi = []

        parzyste = [
            (0, -1),  # Góra
            (0,  1),  # Dół
            (-1, -1), # Lewy-Góra
            (-1,  0), # Lewy-Dół
            (1, -1),  # Prawy-Góra
            (1,  0)   # Prawy-Dół
        ]

        nieparzyste = [
            (0, -1),  # Góra
            (0,  1),  # Dół
            (-1,  0), # Lewy-Góra
            (-1,  1), # Lewy-Dół
            (1,  0),  # Prawy-Góra
            (1,  1)   # Prawy-Dół
        ]

        wybrane_kierunki = parzyste if x % 2 == 0 else nieparzyste

        for dx, dy in wybrane_kierunki:
            nx = x + dx
            ny = y + dy

            if 0 <= nx < self.size_x and 0 <= ny < self.size_y:
                sasiedzi.append(Punkt(nx, ny))

        return sasiedzi