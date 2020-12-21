from collections import namedtuple
from copy import copy

""" ROUGH CODE BELOW:
    THIS DAY IS THE NUMBER 1 IN LIST OF NEEDED REFACTORS.
    VERY INEFFICIENT AND MANY BAD CODE SMELLS.
    ALREADY HAVE AN IDEA USING A DEFAULT-DICT AND MORE EFFICIENT
    TRAVERSING THROUGH THE CUBE, BUT HAVENT HAD MUCH TIME YET
    WHILST KEEPING UP WITH THE NEW PUZZLES AS WELL. """


Cube = namedtuple('Cube', 'x y z active')
Cube4d = namedtuple('Cube4d', 'x y z w active')


def read_input():
    cubes3d = []
    cubes4d = []
    z = w = 0
    with open('solutions/day17/input.txt') as f:
        for y, line in enumerate(f):
            for x, char in enumerate(line.strip()):
                cubes3d.append(Cube(x, y, z, char == '#'))
                cubes4d.append(Cube4d(x, y, z, w, char == '#'))
    return cubes3d, cubes4d


def get_neighbours3d(cube, cubes):
    return list(filter(lambda c: c.x in [cube.x - 1, cube.x, cube.x + 1] and
                       c.y in [cube.y - 1, cube.y, cube.y + 1] and
                       c.z in [cube.z - 1, cube.z, cube.z + 1] and
                       not c == cube, cubes))


def get_bounds3d(cubes):
    min_x = min(map(lambda c: c.x, cubes))
    max_x = max(map(lambda c: c.x, cubes))
    min_y = min(map(lambda c: c.y, cubes))
    max_y = max(map(lambda c: c.y, cubes))
    min_z = min(map(lambda c: c.z, cubes))
    max_z = max(map(lambda c: c.z, cubes))
    return (min_x, max_x), (min_y, max_y), (min_z, max_z)


def expand_cubes3d(xs, ys, zs, cubes):
    for x in range(xs[0] - 1, xs[1] + 2):
        for y in range(ys[0] - 1, ys[1] + 2):
            for z in range(zs[0] - 1, zs[1] + 2):
                if len(list(filter(lambda c: c.x == x and c.y == y and c.z == z, cubes))) == 0:
                    cubes.append(Cube(x, y, z, False))
    return cubes


def cycle3d(cubes):
    xs, ys, zs = get_bounds3d(cubes)
    cubes = expand_cubes3d(xs, ys, zs, cubes)
    new_cubes = []
    for cube in cubes:
        active_neighbours = len(
            list(filter(lambda c: c.active, get_neighbours3d(cube, cubes))))
        if cube.active and active_neighbours in [2, 3]:
            new_cubes.append(cube)
        elif not cube.active and active_neighbours == 3:
            new_cubes.append(Cube(cube.x, cube.y, cube.z, True))
        else:
            new_cubes.append(Cube(cube.x, cube.y, cube.z, False))
    return list(filter(lambda c: c.active, new_cubes))


def get_neighbours4d(cube, cubes):
    return list(filter(lambda c: c.x in [cube.x - 1, cube.x, cube.x + 1] and
                       c.y in [cube.y - 1, cube.y, cube.y + 1] and
                       c.z in [cube.z - 1, cube.z, cube.z + 1] and
                       c.w in [cube.w - 1, cube.w, cube.w + 1] and
                       not c == cube, cubes))


def get_bounds4d(cubes):
    min_x = min(map(lambda c: c.x, cubes))
    max_x = max(map(lambda c: c.x, cubes))
    min_y = min(map(lambda c: c.y, cubes))
    max_y = max(map(lambda c: c.y, cubes))
    min_z = min(map(lambda c: c.z, cubes))
    max_z = max(map(lambda c: c.z, cubes))
    min_w = min(map(lambda c: c.w, cubes))
    max_w = max(map(lambda c: c.w, cubes))
    return (min_x, max_x), (min_y, max_y), (min_z, max_z), (min_w, max_w)


def expand_cubes4d(xs, ys, zs, ws, cubes):
    for x in range(xs[0] - 1, xs[1] + 2):
        for y in range(ys[0] - 1, ys[1] + 2):
            for z in range(zs[0] - 1, zs[1] + 2):
                for w in range(ws[0] - 1, ws[1] + 2):
                    if len(list(filter(lambda c: c.x == x and c.y == y and c.z == z and c.w == w, cubes))) == 0:
                        cubes.append(Cube4d(x, y, z, w, False))
    return cubes


def cycle4d(cubes):
    xs, ys, zs, ws = get_bounds4d(cubes)
    cubes = expand_cubes4d(xs, ys, zs, ws, cubes)
    new_cubes = []
    for cube in cubes:
        active_neighbours = len(
            list(filter(lambda c: c.active, get_neighbours4d(cube, cubes))))
        if cube.active and active_neighbours in [2, 3]:
            new_cubes.append(cube)
        elif not cube.active and active_neighbours == 3:
            new_cubes.append(Cube4d(cube.x, cube.y, cube.z, cube.w, True))
        else:
            new_cubes.append(Cube4d(cube.x, cube.y, cube.z, cube.w, False))
    return list(filter(lambda c: c.active, new_cubes))


cubes3d, cubes4d = read_input()
for i in range(6):
    cubes3d = cycle3d(cubes3d)
    print(f"Completed cycle {i}")
print(len(list(filter(lambda c: c.active, cubes3d))))
for i in range(6):
    cubes4d = cycle4d(cubes4d)
    print(f"Completed cycle {i}")
print(len(list(filter(lambda c: c.active, cubes4d))))
