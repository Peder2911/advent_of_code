"""In my second entry I create a weird solution using itertools and a closure for efficiency!"""
import sys
from typing import Literal, Dict, Iterable, Callable, Tuple, List
import itertools

Shape = Literal["r","p","s"]
RawPlayOpponent = Literal["a","b","c"]
RawPlayPlayer = Literal["x","y","z"]

shapekey = {
    "a":"r",
    "b":"p",
    "c":"s",
    "x":"r",
    "y":"p",
    "z":"s",
}

def shapeseq() -> Iterable[Shape]:
    return itertools.cycle(["r","p","s"])

def windowed_iterate(seq, size):
    current = [*itertools.islice(seq,0,size,1)]
    yield current 
    while True:
        current = current[-(size-1):] + [next(seq)]
        yield current

winseq = windowed_iterate(shapeseq(),3)

def pairing_getter():
    seen = {}
    def _get_pairing(s: Shape):
        if s in seen:
            return seen[s]

        a,b,c = next(winseq)
        if b == s:
            seen[s] = (a,b,c)

        return get_pairing(s)
    return _get_pairing

get_pairing = pairing_getter()

def matchscore(opponent: Shape, player: Shape) -> int:
    result = None 

    if opponent == player:
        return 3

    beats, x, beaten_by = get_pairing(opponent)

    if player == beats:
        return 0
    else:
        return 6

def shapescore(a: Shape,b: Shape) -> int:
    scores: Dict[Shape,int] = {
            "r":1,
            "p":2,
            "s":3,
        }
    return scores[b]

def fix_raw_play(a: RawPlayOpponent,b: RawPlayPlayer):
    opponent_shape = shapekey[a]
    cipher = {k:v for k,v in zip(("x","y","z"),get_pairing(opponent_shape))}
    return opponent_shape, cipher[b]

rules: List[Callable[[Tuple[Shape, Shape]],int]] = [matchscore, shapescore]
score: Callable[[Tuple[Shape,Shape]], int] = lambda a,b: sum(map(lambda f: f(a,b), rules))

if __name__ == "__main__":
    raw_plays = [[s.lower() for s in ln.split()] for ln in sys.stdin.readlines()]
    plays = [[shapekey[s] for s in p] for p in raw_plays]
    scores = list(map(lambda play: score(*play), plays))

    print(f"Total score: {sum(scores)}")

    fixed_plays = list(map(lambda p: fix_raw_play(*p), raw_plays))
    fixed_scores = list(map(lambda play: score(*play), fixed_plays))

    print(f"Fixed score: {sum(fixed_scores)}")
