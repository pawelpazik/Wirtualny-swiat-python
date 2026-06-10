import json
import sys
from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from src.swiat.Swiat import Swiat


class MenedzerZapisu:
    SCIEZKA_ZAPISU = "zapis_gry.json"

    @staticmethod
    def zapisz_gre(swiat: 'Swiat'):
        try:
            organizmy_dane = []

            for org in swiat.get_organizmy():
                if org.czy_zyje():
                    dane_org = {
                        "nazwaGatunku": org.get_nazwa(),
                        "x": org.get_x(),
                        "y": org.get_y(),
                        "sila": org.get_sila(),
                        "wiek": org.get_wiek()
                    }

                    if type(org).__name__ == "Czlowiek":
                        dane_org["czas_tarczy"] = org.get_czas_tarczy()
                        dane_org["cooldown"] = org.get_cooldown()

                    organizmy_dane.append(dane_org)

            stan_gry = {
                "rozmiarX": swiat.get_size_x(),
                "rozmiarY": swiat.get_size_y(),
                "czyHex": swiat.czy_hex(),
                "organizmy": organizmy_dane
            }

            with open(MenedzerZapisu.SCIEZKA_ZAPISU, 'w', encoding='utf-8') as plik:
                json.dump(stan_gry, plik, indent=4)

            print("Gra została pomyślnie zapisana.")

        except Exception as e:
            print(f"Błąd podczas zapisywania gry: {e}", file=sys.stderr)

    @staticmethod
    def wczytaj_gre() -> Optional['Swiat']:
        try:
            with open(MenedzerZapisu.SCIEZKA_ZAPISU, 'r', encoding='utf-8') as plik:
                stan_gry = json.load(plik)

            rozmiar_x = stan_gry["rozmiarX"]
            rozmiar_y = stan_gry["rozmiarY"]
            czy_hex = stan_gry["czyHex"]

            from src.swiat.SwiatHex import SwiatHex
            from src.swiat.SwiatSiatka import SwiatSiatka

            if czy_hex:
                nowy_swiat = SwiatHex(rozmiar_x, rozmiar_y)
            else:
                nowy_swiat = SwiatSiatka(rozmiar_x, rozmiar_y)

            nowy_swiat.generowanie = True

            organizmy_dane = stan_gry.get("organizmy", [])
            for dane in organizmy_dane:
                org = nowy_swiat.get_konstruktor_do_odczytu(
                    dane["nazwaGatunku"],
                    dane["x"],
                    dane["y"],
                    dane["sila"],
                    dane["wiek"]
                )

                if org is not None:
                    if type(org).__name__ == "Czlowiek":
                        czas = dane.get("czas_tarczy", 0)
                        cd = dane.get("cooldown", 0)
                        org.wczytaj_stan_tarczy(czas, cd)

                    nowy_swiat.dodaj_nowy_organizm(org)

            nowy_swiat.generowanie = False
            print("Gra została pomyślnie wczytana z pliku JSON.")
            return nowy_swiat

        except FileNotFoundError:
            print("Nie znaleziono pliku zapisu 'zapis_gry.json'.", file=sys.stderr)
            return None
        except Exception as e:
            print(f"Błąd podczas wczytywania gry: {e}", file=sys.stderr)
            return None