class RejestrGatunkow:
    _gatunki = {
        "Czlowiek": "src.organizmy.zwierzeta.Czlowiek.Czlowiek",
        "Trawa": "src.organizmy.rosliny.Trawa.Trawa",
        "Barszcz Sosnowskiego": "src.organizmy.rosliny.BarszczSosonowskiego.BarszczSosnowskiego",
        "Wilk": "src.organizmy.zwierzeta.Wilk.Wilk",
        "Owca": "src.organizmy.zwierzeta.Owca.Owca",
        "Guarana": "src.organizmy.rosliny.Guarana.Guarana",
        "Lis": "src.organizmy.zwierzeta.Lis.Lis",
        "Zolw": "src.organizmy.zwierzeta.Zolw.Zolw",
        "Cyber Owca": "src.organizmy.zwierzeta.CyberOwca.CyberOwca",
        "Mlecz": "src.organizmy.rosliny.Mlecz.Mlecz",
        "Wilcze Jagody": "src.organizmy.rosliny.WilczeJagody.WilczeJagody",
        "Antylopa": "src.organizmy.zwierzeta.Antylopa.Antylopa",
    }

    @classmethod
    def get_nazwy_klas(cls) -> dict:
        return cls._gatunki