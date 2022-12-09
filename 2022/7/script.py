
import sys
from operator import add
from typing import Callable,Dict,List,Union
from functools import reduce

SMALL_DIR = 100_000
NEEDED_SPACE = 30_000_000
FS_SIZE= 70_000_000
data = sys.stdin.readlines()

TdlNode= Dict[str,Union[int,"TdlNode"]]
TdlOp= Callable[[List[str],TdlNode], None]

compose = lambda a,b: lambda *args,**kwargs: b(a(*args,**kwargs))
no_op = lambda *args,**kwargs: None

class Node():
    def __init__(self, values: TdlNode, name: str = ""):
        self._values: TdlNode = values
        self.name = name

    @property
    def children(self):
        return [Node(values = v, name = k) for k,v in self._values.items() if isinstance(v, dict)]

    @property
    def values(self):
        return [v for v in self._values.values() if not isinstance(v, dict)]

    def map(self, fn, red, init):
        return red(fn(self.values), reduce(red, [child.map(fn,red,init) for child in self.children], init))

    def walk(self):
        yield self
        for child in self.children:
            yield from child.walk()

    def __repr__(self):
        return f"A node with {len(self.children)} children and {len(self.values)} values."

def compose_mutate(a,b):
    def inner(*args, **kwargs):
        a(*args,**kwargs)
        b(*args,**kwargs)
    return inner

def empty(l):
    while l:
        l.pop()

def assign_into(path, tree, element) -> None:
    if len(path) == 1:
        tree[path[0]] = element
    else:
        assign_into(path[1:], tree.get(path[0], {}), element)

def compile_path_operations(path_elements) -> TdlOp:
    def path_operation(el):
        down = lambda cwd,_: cwd.append(el)
        up = lambda cwd,_: cwd.pop()
        root = lambda _,__: empty(cwd)

        if el == "..":
            return up
        elif el == "/":
            return root
        else:
            return down

    reversed(path_elements)
    return reduce(compose_mutate, map(path_operation, path_elements), no_op)

def parse_cmd(command, args = []) -> TdlOp:
    if command == "cd":
        try:
            path_elements = [el for el in args[0].split("/") if el]
            return compile_path_operations(path_elements)
        except KeyError:
            raise ValueError(f"cd was invoked without an argument: {command} {args}")
    elif command == "ls":
        return no_op
    else:
        raise ValueError(f"Unknown command: {command}")

def parse_dcl(kind, name) -> TdlOp:
    if kind == "dir":
        return lambda cwd,tree: assign_into(cwd+[name], tree, {})
    else:
        try:
            size = int(kind)
        except ValueError:
            raise ValueError(f"Found weird declaration: {kind} {name}")
        return lambda cwd,tree: assign_into(cwd+[name], tree, size)

def parse(line) -> TdlOp:
    kind, *rest = line.split()
    if kind == "$":
        cmd, *args = rest
        return parse_cmd(cmd, args)
    else:
        name, *_ = rest
        return parse_dcl(kind,name)

def traversible(node):
    children = {k:v for k,v in tree.items() if isinstance(v, dict)}
    leaves = [v for v in tree.values() if not isinstance(v, dict)]
    return leaves, children

cwd=[]
tree={}
for line in data:
    op = parse(line)
    op(cwd,tree)

node_sums = [node.map(sum,add,0) for node in Node(tree).walk()]
total_size = max(node_sums)
small_dirs_sum = sum([s for s in node_sums if s < SMALL_DIR])
print(small_dirs_sum)
free_space = FS_SIZE - total_size
need_to_delete = (NEEDED_SPACE-free_space)
to_delete = min([s for s in node_sums if s > need_to_delete])

print(f"Sum of small directories: {small_dirs_sum}")
print(f"Size of deletion candidate: {to_delete}")
