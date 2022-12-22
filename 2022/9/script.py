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
TRAIL = "."
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
    number,direction = cmd
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
    #hx,hy = int(rows/2), int(columns/2)
    translate = lambda crds: vadd(vsub(crds, entities[HEAD][0]), [int(rows/2), int(columns/2)]) #vsub([int(rows/2), int(columns/2)], crds)

    screen_rect = [[0,0], [rows, columns]]

    for symbol,coords in entities.items():
        for x,y in coords:
            x,y = translate([x,y]) 
            if rcontains(screen_rect, [x,y]):
                data[x][y] = symbol

    return data

def simulate(move, entities):
    old_head = entities[HEAD][0]
    new_head = vadd(old_head, move)
    entities[HEAD][0] = new_head

    old_tail = entities[TAIL][0]
    xdist,ydist = vabs(vsub(old_tail,new_head))
    if xdist>1 or ydist>1:
        entities[TAIL][0] = [v for v in old_head] 

    entities[TRAIL].append(entities[TAIL][0])

    return entities

commands = reduce(add, [list(steps(parse(random_command()))) for _ in range(100)])

entities = OrderedDict({
       #"-":[[0,i] for i in range(-100,100)],
       #"|":[[i,0] for i in range(-100,100)],
       #"o": [[0,0]], 
        TRAIL: [], 
        HEAD: [[0,0]], 
        TAIL: [[0,0]],
        })
for move in commands:
    entities = simulate(move, entities)
    blit(grid(entities))
    time.sleep(.05)
