import sys
import copy
from collections import defaultdict

class Cpu():

    def __init__(self):
        self.cycle = 0
        self.x = 1
        self.result = 0
        self.pixels = defaultdict(lambda: ["." for _ in range(40)]) 

    def addx(self,v):
        self.iterate_cycle(2)
        self.x += int(v)

    def noop(self):
        self.iterate_cycle(1)

    def iterate_cycle(self, i = 1):
        self.cycle += 1
        
        x,y = self.position
        self.pixels[x][y]
        if (x,y) in set(self.sprite):
            self.pixels[x][y] = "#"

        if (self.cycle - 20) % 40 == 0:
            self.result += self.signal_strength
        if i > 1:
            self.iterate_cycle(i -1)

    def show_screen(self, with_sprite: bool = False):
        pixels = copy.deepcopy(self.pixels)
        if with_sprite:
            for cs in self.sprite:
                x,y = cs
                pixels[x][y] = "$"
        print("\n".join(["".join(pixels[v]) for v in range(len(pixels))]))

    def display(self):
        self.show_screen()
        print(f"Result = {self.result}")

    def execute(self, cmd, args):
        getattr(self, cmd)(*args)

    @property
    def signal_strength(self):
        return self.cycle * self.x

    @property
    def sprite(self):
        return [(self.row,v) for v in range(self.x-1, self.x+2)]

    @property
    def row(self):
        return (self.cycle-1) // 40

    @property
    def column(self):
        return (self.cycle-1) % 40

    @property
    def position(self):
        return self.row, self.column 

def parse(line):
    cmd, *args = line.split()
    return cmd, args

cpu = Cpu()
for i,line in enumerate(sys.stdin.readlines()):
    cmd, args = parse(line)
    cpu.execute(cmd, args)

cpu.display()
