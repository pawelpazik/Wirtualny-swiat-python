class BarszczSosnowskiego(Roslina):

    def __init__(self, swiat: Swiat, x: int, y: int):
        super().__init__(swiat, x, y, 10, 0)

    def __init__(self, swiat: Swiat, x: int, y: int, sila: int, wiek: int):
        super().__init__(swiat, x, y, sila, 0)
        self.wiek = wiek


    def akcja(self):
        wiek += 1
        polaWokol = swiat.getSasiedniePola(x, y)
        for p in polaWokol:
            xO = p.getX()
            yO = p.getY()
            ofiara = swiat.getOrganizmyNaPolu(xO, yO)
            if (type(ofiara) is Zwierze) and ofiara.czyZyje():
                if not ofiara.odpornyNaBarszcz():
                    ofiara.zabij()
                    swiat.dodajLog(this.getNazwa() + "zabija zwierze w poblizu: " + ofiara.getNazwa())

    def kolizja(self, drugi: Organizm):
        if type(drugi) is Zwierze:
            if drugi.czyUcieka():
                drugi.przesunNaPuste()
                swiat.dodajLog(drugi.getNazwa() + "ucieka przed: " + this.getNazwa())
                return
            if not drugi.odpornyNaBarszcz():
                drugi.zabij()
                swiat.dodajLog(drugi.getNazwa() + " zjadl " + this.getNazwa() + " i umiera");
                return

            swiat.dodajLog(napastnik.getNazwa() + " zjadl " + this.getNazwa());
            this.zabij();

    def stworzNowy(self, x: int, y: int) -> Organizm:
        return BarszczSosnowskiego(self.swiat, x, y)

    def getNazwa(self) -> str:
        return "Barszcz Sosnowskiego"

    def getZnak(self) -> str:
        return 'B'

    def getKolor(self) -> str:
        return "#d8ffbf"
