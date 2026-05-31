from src.swiat.Swiat import Swiat
from src.swiat.Punkt import Punkt

class SwiatSiatka(Swiat):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    def czy_hex(self) -> bool:
        return False

    def get_sasiednie_pola(self, x: int, y: int):
        sasiedzi = []

        kierunki = [
            (-1, -1), (0, -1), (1, -1),
            (-1,  0),          (1,  0),
            (-1,  1), (0,  1), (1,  1)
        ]

        for dx, dy in kierunki:
            nx = x + dx
            ny = y + dy

            if 0 <= nx < self.size_x and 0 <= ny < self.size_y:
                sasiedzi.append(Point(nx, ny))

        return sasiedzi