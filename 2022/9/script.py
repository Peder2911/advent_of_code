import time
from typing import Literal, Union
from collections import OrderedDict
import random
from operator import add, mul, sub
from functools import reduce, partial
import os
import sys

Direction = Union[Literal["U"], Literal["R"], Literal["D"], Literal["L"]]
HEAD = "O"
TAIL = "z"
ROPE = "*"
TRAIL_FIRST = "."
TRAIL_LAST = ","
EMPTY = " "

def vop(fn, a, b):
    return reduce(lambda a,b: a + [reduce(fn, b)], zip(a,b), [])

vadd = partial(vop, add)
vmul = partial(vop, mul)
vsub = partial(vop, sub)

vinv = lambda vs: [-v for v in vs] 
vabs = lambda vs: [abs(v) for v in vs] 

def rcontains(rect, point):
    upper_left, bottom_right = rect
    x,y = point

    return all([
            upper_left[0] < x,
            upper_left[1] < y,
            bottom_right[0] > x,
            bottom_right[1] > y,
            ])

def parse(cmd):
    direction, number = cmd.split()
    magnitude = int(number)
    return vmul(direction_to_vector(direction), [magnitude, magnitude])

def direction_to_vector(direction):
    return {
        "U":[0,1],
        "R":[1,0],
        "D":[0,-1],
        "L":[-1,0],
    }[direction]

def diminish(integer: int) -> int:
    if integer > 0:
        return -1
    elif integer < 0:
        return 1
    else:
        return 0

def steps(vector):
    if not all([v == 0 for v in vector]):
        next_vector = [diminish(v) for v in vector]
        yield next_vector
        yield from steps(vsub(vector, vinv(next_vector)))

def random_command():
    directions = "LURD"
    number = int(abs(random.normalvariate(0,1))*2)+1
    direction = random.choice(directions)
    return "".join((str(number), direction)) 

def blit(data):
    for row in data:
        for symbol in row:
            sys.stdout.write(symbol)
        sys.stdout.write("\n")

def grid(entities):
    columns,rows = os.get_terminal_size()
    data = [[EMPTY for _ in range(columns)] for __ in range(rows)]
    translate = lambda crds: vadd(vsub(crds, entities[ROPE][0]), [int(rows/2), int(columns/2)])

    screen_rect = [[0,0], [rows, columns]]

    for symbol,coords in entities.items():
        for x,y in coords:
            x,y = translate([x,y]) 
            if rcontains(screen_rect, [x,y]):
                data[x][y] = symbol

    return data

def sign(x):
    if x < 0:
        return -1
    elif x > 0:
        return 1
    return 0



def rope(links, move):
    links[0] = vadd(links[0], move)
    for a,b in ((n-1, n) for n in range(1,len(links))):
        head,tail = links[a], links[b]
        distance = vsub(head,tail)
        move = [v-sign(v) for v in distance]
        links[b] = vadd(tail,move) 
    return links

def simulate(move, entities):
    entities[ROPE] = rope(entities[ROPE], move)
    entities[TRAIL_FIRST].append(entities[ROPE][1])
    entities[TRAIL_LAST].append(entities[ROPE][-1])

    return entities

display = False
try:
    display = sys.argv[1] == "--display"
except IndexError:
    pass 

commands = reduce(add, [list(steps(parse(ln))) for ln in sys.stdin.readlines()])

entities = OrderedDict({
        "-":[[0,i] for i in range(-100,100)],
        "|":[[i,0] for i in range(-100,100)],
        "o": [[0,0]], 
        TRAIL_FIRST: [], 
        TRAIL_LAST: [], 
        ROPE: [[0,0] for _ in range(10)],
        })

for move in commands:
    entities = simulate(move, entities)
    if display:
        blit(grid(entities))
        time.sleep(.1)

print(f"First trail: {len({tuple(c) for c in entities[TRAIL_FIRST]})}")
print(f"Last trail: {len({tuple(c) for c in entities[TRAIL_LAST]})}")
