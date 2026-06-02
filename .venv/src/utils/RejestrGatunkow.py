class RejestrGatunkow:
    # Słownik (odpowiednik Map z Javy) przechowujący ścieżki do plików.
    # Wzór: "NazwaGatunku": "folder.folder.Plik.Klasa"
    _gatunki = {
        "Czlowiek": "src.organizmy.zwierzeta.Czlowiek.Czlowiek",
        "Trawa": "src.organizmy.rosliny.Trawa.Trawa",
        "Barszcz Sosnowskiego": "src.organizmy.rosliny.BarszczSosonowskiego.BarszczSosnowskiego",
        "Wilk": "src.organizmy.zwierzeta.Wilk.Wilk",
        "Owca": "src.organizmy.zwierzeta.Owca.Owca"
    }

    @classmethod
    def get_nazwy_klas(cls) -> dict:
        return cls._gatunki