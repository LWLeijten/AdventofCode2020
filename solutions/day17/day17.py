from collections import defaultdict
from itertools import product
import operator


def read_input():
    """ Reads the input file and returns it as a default dict 
        containing active cubes, for both 3d and 4d space. """
    cubes3d = defaultdict(lambda: 0)
    cubes4d = defaultdict(lambda: 0)
    z = w = 0
    with open('solutions/day17/input.txt') as f:
        for y, line in enumerate(f):
            for x, char in enumerate(line.strip()):
                if char == '#':
                    cubes3d[(x, y, z)] = 1
                    cubes4d[(x, y, z, w)] = 1
    return cubes3d, cubes4d


def get_neighbours(cube):
    """ Gets all the neighbours of a cube, agnostic to the amount of dimensions. 
        Remove the cube itself as a neighbour as final step."""
    neighbours = []
    for direction in product([-1, 0, 1], repeat=len(cube)):
        neighbours.append(tuple(map(operator.add, cube, direction)))
    neighbours.remove(cube)
    return neighbours


def get_relevant_cubes(cube_dict):
    """ Creates a set of cubes that we have to check the
        game of life rules against for a given round. """
    actives = list(cube_dict.keys())
    neighbours = set()
    for a in actives:
        nbs = get_neighbours(a)
        for nb in nbs:
            neighbours.add(nb)
    targets = actives + list(neighbours)
    return targets


def simulate_round(cube_dict):
    """ Simulates a round of the game of life.
        First find the target cubes, secondly check them against the decision rules.
        Returns a dict of only active cubes after the round is over. """
    targets = get_relevant_cubes(cube_dict)
    output_dict = defaultdict(lambda: 0)
    for t in targets:
        is_active = cube_dict[t]
        a_neighbours = len(
            list(filter(lambda nb: cube_dict[nb] == 1, get_neighbours(t))))
        if is_active and a_neighbours in [2, 3]:
            output_dict[t] = 1
        elif not is_active and a_neighbours == 3:
            output_dict[t] = 1
    return output_dict


# Find the solutions for part 1 and 2 of the puzzle.
if __name__ == "__main__":
    cubes3d, cubes4d = read_input()
    for i in range(6):
        cubes3d = simulate_round(cubes3d)
        print(f"Completed cycle {i}")
    print(len(cubes3d))
    for i in range(6):
        cubes4d = simulate_round(cubes4d)
        print(f"Completed cycle {i}")
    print(len(cubes4d))
