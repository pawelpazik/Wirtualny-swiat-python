from abc import ABC, abstractmethod

class Organizm(ABC):
    def __init__(self, swiat, x, y, sila, inicjatywa):
        this.swiat = swiat;
        this.x = x;
        this.y = y;
        this.sila = sila;
        this.inicjatywa = inicjatywa;
        this.wiek = 0;
        this.zyje = true;

    @abstractmethod
    def akcja(self):
        pass

    @abstractmethod
    def kolizja(self, organizmDrugi):
        pass

    @abstractmethod
    def getNazwa(self):
        pass

    @abstractmethod
    def stworzNowy(self) -> organizmDrugi:
        pass

    def czyucieka(self) -> bool:
        return False;

    def czyOdbilAtak(self, napastnik) -> bool:
        return False;

    def getSila(self):
        return self.sila;

    def setSila(self, sila):
        self.sila = sila;

    def getInicjatywa(self):
        return self.inicjatywa;

    def getX(self):
        return self.x;

    def getY(self):
        return self.y;

    def getWiek(self):
        return self.wiek;

    def czyZyje(self):
        return self.zyje;

    def zabij(self):
        self.zyje = false;

    @abstractmethod
    def getZnak(self):
        pass

    @abstractmethod
    def getColor(self):
        pass