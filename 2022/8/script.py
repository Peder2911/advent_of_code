"""Convoluted solution with lots of unused, but fun functions for working with matrices!"""
import sys
from functools import reduce
from operator import add, mul

def printmat(mat):
    print("\n".join(["".join([str(c) for c in ln]) for ln in mat]))

def look_at_row(row):
    """Returns the Y coordinate of the tallest tree seen from the left."""
    biggest_so_far = -1
    indices_of_seen = []
    for i,number in enumerate(row):
        if number > biggest_so_far:
            biggest_so_far = number
            indices_of_seen.append(i)
    return indices_of_seen 

def look_at_matrix(mat):
    """Returns the X,Y coordinates of the tallest trees seen from the left."""
    indices = set() 
    for x,row in enumerate(mat):
        indices = indices.union({(x,i) for i in look_at_row(row)})
    return indices

def matrix_map(fn,mat):
    return [[fn((x,y),v) for y,v in enumerate(r)] for x,r in enumerate(mat)]

def transpose(mat):
    xs = len(mat)
    ys = len(mat[0])
    return [[mat[x][y] for x in range(xs-1,-1,-1)] for y in range(ys)]

def transpose_coords(turns, size_x, size_y, coords):
    turns = turns % 4
    x,y = coords
    match turns:
        case 0:
            return (x,y)
        case 1:
            return (size_y - y, x)
        case 2:
            return (y,x)
        case 3:
            return (y, size_x - x)

def can_see_from_left(mat):
    seen = look_at_matrix(mat)
    return matrix_map(lambda crds,_: True if crds in seen else False, mat)

def display(mat):
    return matrix_map(lambda _,v: "x" if v else ".", mat)

def matrix_reduce(fn, a,b):
    return [[fn(ya,yb) for ya,yb in zip(xa,xb)] for xa,xb in zip(a,b)] 

def filled(v,xs,ys):
    return [[v for _ in range(ys)] for __ in range(xs)]

def dims(mat):
    return len(mat[0]), len(mat)

def flatten(mat):
    return list(reduce(add, mat))

def values_starting_from(coords, mat):
    xs,ys = dims(mat)
    x_start, y_start = coords
    coords = [
            [(x,y_start) for x in range(x_start-1,-1,-1)],
            [(x_start,y) for y in range(y_start+1,ys)],
            [(x,y_start) for x in range(x_start+1,xs)],
            [(x_start,y) for y in range(y_start-1,-1,-1)],
        ]
    return [[mat[x][y] for x,y in crds] for crds in coords]

def is_visible(coordinates,tree_height,matrix):
    def visible(from_height, trees):
        for tree in trees:
            if tree >= from_height:
                return False
        return True
    return any([visible(tree_height,values) for values in values_starting_from(coordinates, matrix)])

def scenic_score(coordinates,tree_height,matrix):
    def score_in_direction(from_height, trees):
        value = 0
        for tree in trees:
            value += 1
            if tree >= from_height:
                break
        return value
    return reduce(mul,([score_in_direction(tree_height,values) for values in values_starting_from(coordinates, matrix)]))

data = sys.stdin.readlines()
matrix = [[int(c) for c in ln.strip()] for ln in data]
xs,ys = dims(matrix)


visible = matrix_map(lambda crds,val: is_visible(crds, val, matrix), matrix)
scenic_scores = matrix_map(lambda crds,val: scenic_score(crds, val, matrix), matrix)
printmat(display(visible))
print(f"Visible trees: {sum(flatten(visible))}\tMax scenic score: {max(flatten(scenic_scores))}")
