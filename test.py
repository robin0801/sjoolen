BEURTEN_PER_RONDE = 4 - 1  # 3 beurten per ronde
POORTJES = 4
PUNTEN_PER_SET = 20


class Speler:
    def __init__(self, naam, totaal_score=0):
        self.__naam = naam
        self.__scores = []  # score per ronde
        self.__totaal_score = totaal_score

    def add_scores(self, score):
        self.__scores.append(score)
        self.set_totaal_score(self.__totaal_score + score)

    def set_totaal_score(self, totaal_score):
        self.__totaal_score = totaal_score

    def get_naam(self):
        return self.__naam

    def get_scores(self):
        return self.__scores

    def get_totaal_score(self):
        return self.__totaal_score

    def get_max_score(self):
        return max(self.__scores) if self.__scores else 0

    def get_min_score(self):
        return min(self.__scores) if self.__scores else 0

    def get_gemiddelde(self):
        return sum(self.__scores) / len(self.__scores) if self.__scores else 0


def vraag_getal(vraag):
    """Blijft vragen tot er een geldig geheel getal (0 of hoger) is ingevoerd."""
    while True:
        try:
            val = int(input(vraag))
            if val < 0:
                print("  Een negatief aantal kan niet, probeer opnieuw.")
                continue
            return val
        except ValueError:
            print("  Dat is geen getal, probeer opnieuw.")


def score_toevoegen():
    """Vraagt de stenen per poortje voor één beurt. Geeft de lijst terug."""
    scored = []
    for i in range(1, POORTJES + 1):
        scored.append(vraag_getal(f"  Hoeveel stenen heb je op de {i} plek: "))
    return scored


def score_berekenen(scored):
    """Berekent de score van één beurt."""
    laagste_val = min(scored)
    score = laagste_val * PUNTEN_PER_SET
    for a, waardes in enumerate(scored, start=1):
        score += (waardes - laagste_val) * a
    return score


def ronde_spelen(spelers):
    for speler in spelers:
        print(f"\n--- {speler.get_naam()} is aan de beurt ---")
        print(f"Vul het totaal aantal stenen van alle {BEURTEN_PER_RONDE} beurten in.")
        scored = score_toevoegen()
        ronde_score = score_berekenen(scored)
        speler.add_scores(ronde_score)
        print(f"\n{speler.get_naam()} scoorde {ronde_score} punten deze ronde.")


def tussenstand(spelers):
    gesorteerd = sorted(spelers, key=lambda s: s.get_totaal_score(), reverse=True)
    print(f"\n{'#':<3}{'Naam':<20}{'Max':>6}{'Min':>6}{'Gem.':>8}{'Totaal':>9}")
    print("-" * 52)
    for plek, s in enumerate(gesorteerd, start=1):
        print(f"{plek:<3}{s.get_naam():<20}{s.get_max_score():>6}"
              f"{s.get_min_score():>6}{round(s.get_gemiddelde()):>8}{s.get_totaal_score():>9}")


def spelers_aanmaken():
    spelers = []
    while True:
        naam = input("Geef de naam van een speler: ").strip()
        if not naam:
            if spelers:
                break
            print("  Je hebt minstens één speler nodig.")
            continue
        spelers.append(Speler(naam))
    return spelers


def spel_starten(spelers):
    while True:
        ronde_spelen(spelers)
        print("\n=== Ronde klaar ===")
        while True:
            keuze = input("\nWat nu? [1] Nog een ronde  [2] Tussenstand  [3] Afsluiten: ").strip()
            if keuze == "1":
                break
            elif keuze == "2":
                tussenstand(spelers)
            elif keuze == "3":
                print("\nEindstand:")
                tussenstand(spelers)
                return
            else:
                print("  Kies 1, 2 of 3.")


def main():
    print("\nWelkom bij deze score app \nMaak een nieuwe speler lijst aan\n"
          "Typ de naam en druk op ENTER, \ngeef geen input als je het spel wilt beginnen")
    spelers = spelers_aanmaken()
    spel_starten(spelers)


if __name__ == "__main__":
    main()