from logging import NullHandler

from src.organizmy.zwierzeta.Zwierze import Zwierze


class Czlowiek(Zwierze):
    def __init__(self, swiat, x: int, y: int, sila: int = 5, wiek: int = 0, trwanie_umiejetnosci: int = 0, cooldown_umiejetnosci: int = 0):
        super().__init__(swiat, x, y, sila, 4)
        self.wiek = wiek
        self.trwanie_umiejetnosci = trwanie_umiejetnosci
        self.cooldown_umiejetnosci = cooldown_umiejetnosci
        self.wektor_ruchu_x = 0
        self.wektor_ruchu_y = 0

    def ustaw_kierunek_ruchu(self, dx: int, dy: int):
        self.wektor_ruchu_x = dx
        self.wektor_ruchu_y = dy

    def aktywuj_umiejetnosc(self):
        if self.cooldown_umiejetnosci == 0 and self.trwanie_umiejetnosci == 0:
            self.trwanie_umiejetnosci = 5
            self.cooldown_umiejetnosci = 5
            self.swiat.dodaj_log("Człowiek aktywował Tarczę Alzura!")
            self.swiat.dodaj_log("Tarcza Alzura aktywna (" + str(self.trwanie_umiejetnosci) + " tur)")
        else:
            self.swiat.dodaj_log("Umiejętność jeszcze się ładuje...")

    def akcja(self):
        self.wiek += 1
        self.p_x = self.x
        self.p_y = self.y

        if self.trwanie_umiejetnosci > 0:
            self.trwanie_umiejetnosci -= 1
            self.swiat.dodaj_log("Tarcza Alzura aktywna (" + str(self.trwanie_umiejetnosci) + " tur)")
        elif self.cooldown_umiejetnosci > 0:
            self.swiat.dodaj_log("Tarcza zablokowana (" + str(self.cooldown_umiejetnosci) + " tur)")
            self.cooldown_umiejetnosci -= 1
        else:
            self.swiat.dodaj_log("Tarcza dostępna!")

        if self.wektor_ruchu_x != 0 or self.wektor_ruchu_y != 0:
            potencjalny_ruch_x = self.x + self.wektor_ruchu_x
            potencjalny_ruch_y = self.y + self.wektor_ruchu_y

            sasiedzi = self.swiat.get_sasiednie_pola(self.x, self.y)
            poprawny_ruch = False

            for p in sasiedzi:
                if p.x == potencjalny_ruch_x and p.y == potencjalny_ruch_y:
                    poprawny_ruch = True
                    break

            if poprawny_ruch:
                self.swiat.przesun_na_planszy(self, potencjalny_ruch_x, potencjalny_ruch_y)
                self.x = potencjalny_ruch_x
                self.y = potencjalny_ruch_y
            else:
                self.swiat.dodaj_log("Człowiek uderzył w krawędź świata!")

            self.wektor_ruchu_x = 0
            self.wektor_ruchu_y = 0


    def czy_odbil_atak(self, napastnik: 'Organizm') -> bool:
        if self.trwanie_umiejetnosci > 0:
            self.swiat.dodaj_log("Tarcza Alzura odbiła atak " + napastnik.get_nazwa() + "!")
            return True
        else:
            return False

    def stworz_nowy(self, x: int, y: int) -> 'Organizm':
        return None

    def get_kolor(self) -> str:
        if self.trwanie_umiejetnosci > 0:
            return "#4ce2f5"
        return "#4c5df5"

    def czy_jest_drapieznikiem(self) -> bool:
        return True

    def get_nazwa(self) -> str:
        return "Czlowiek"

    def get_znak(self) -> str:
        return '&'

    def get_czas_tarczy(self) -> int:
        return self.trwanie_umiejetnosci

    def get_cooldown(self) -> int:
        return self.cooldown_umiejetnosci

    def wczytaj_stan_tarczy(self, czas: int, cd: int):
        self.trwanie_umiejetnosci = czas
        self.cooldown = cd
