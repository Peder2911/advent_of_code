import dataclasses

@dataclasses.dataclass
class Card:
    numbers: list[int]
    winning_numbers: list[int]
    copies: int = 1

    @property
    def wins(self) -> int:
        return len(set(self.winning_numbers).intersection(set(self.numbers)))

    @property
    def score(self) -> int:
        score = 0
        for number in self.numbers:
            if number in self.winning_numbers:
                if score == 0:
                    score = 1
                else:
                    score *= 2
        return score

def parse_line(line: str) -> Card:
    line = line[line.index(":")+1:]
    parse_numbers = lambda ns: [int(n.strip()) for n in ns.split()]
    return Card(**{k:parse_numbers(ns) for k,ns in zip(("winning_numbers","numbers"),line.split("|"))})


if __name__ == "__main__":
    with open("data") as f:
        cards = [parse_line(ln) for ln in f.readlines()]
    print(f"Task 1: {sum([c.score for c in cards])}")

    for i,card in enumerate(cards):
        wins = card.wins
        if wins:
            for n in range(card.copies):
                for j in range(wins):
                    cards[i+(j+1)].copies += 1

    print(f"Task 2: {sum([c.copies for c in cards])}")
            
