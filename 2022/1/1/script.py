from functools import reduce; import sys
elves = list(map(sum, reduce(lambda a,b: a + [[]] if b == "" else a[:-1] + [(a[-1] if a else []) + [b]], [int(l) if l else "" for l in [r.strip() for r in sys.stdin.readlines()]], [])))
print(f"Max: {max(elves)} Topthree: {sum(sorted(elves)[-3:])}")
