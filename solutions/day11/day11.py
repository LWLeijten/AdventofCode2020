from copy import deepcopy
from itertools import product


def read_input():
    """Reads the input of the problem and returns it as a matrix of seats"""
    matrix = []
    with open('solutions/day11/input.txt') as f:
        for line in f:
            row = []
            for char in line.strip('\n'):
                row.append(char)
            matrix.append(row)
    return matrix


def get_adjacent_directions():
    """ Returns the possible directions you can look at from a chair. """
    directions = [p for p in product([-1, 0, 1], repeat=2)]
    directions.remove((0, 0))
    return directions


def get_new_seat(x, y, x_step, y_step, distance=1):
    """ Returns the new x and y of a seat. 
        Given the current x,y, the x and y steps and the distance to look at. """
    return x + x_step * distance, y + y_step * distance


def coordinate_in_matrix(matrix, x, y):
    """ Returns whether or not the x and y values fall within the bounds of the matrix. """
    return all([x >= 0, x < len(matrix[0]), y >= 0, y < len(matrix)])


def occupied_adjacents(matrix, seat_y, seat_x):
    """ Returns the amount of occupied seats adjacent to the given seat. """
    adjacents = 0
    directions = get_adjacent_directions()
    for x_step, y_step in directions:
        new_x, new_y = get_new_seat(seat_x, seat_y, x_step, y_step)
        if coordinate_in_matrix(matrix, new_x, new_y):
            adjacents += matrix[new_y][new_x] == '#'
    return adjacents


def occupied_visibles(matrix, seat_y, seat_x):
    """ Returns the amount of occupied seats visible from the given seat. """
    adjacents = 0
    directions = get_adjacent_directions()
    for x_step, y_step in directions:
        distance = 1
        new_x, new_y = get_new_seat(seat_x, seat_y, x_step, y_step, distance)
        while coordinate_in_matrix(matrix, new_x, new_y):
            seat = matrix[new_y][new_x]
            if seat == '#' or seat == 'L':
                adjacents += seat == '#'
                break
            else:
                distance += 1
                new_x, new_y = get_new_seat(
                    seat_x, seat_y, x_step, y_step, distance)
    return adjacents


def simulate(matrix, visibility, tolerance):
    """ Runs the simulation given a matrix of seats, a visibility function and a tolerance threshold.
        Returns the amount of occupied chairs at the equilibrium. """
    mutations = False
    new_matrix = deepcopy(matrix)
    for y in range(len(matrix)):
        for x in range(len(matrix[0])):
            adjacents = visibility(matrix, y, x)
            seat = matrix[y][x]
            if seat == 'L' and adjacents == 0:
                new_matrix[y][x] = '#'
                mutations = True
            elif seat == '#' and adjacents >= tolerance:
                new_matrix[y][x] = 'L'
                mutations = True
    if mutations:
        return simulate(new_matrix, visibility, tolerance)
    else:
        return sum(map(lambda r: r.count('#'), new_matrix))


# Find the solutions for part 1 and 2 of the puzzle.
if __name__ == "__main__":
    matrix = read_input()
    print(
        f"Amount of occupied seats in part 1: {simulate(matrix, occupied_adjacents, 4)}")
    print(
        f"Amount of occupied seats in part 2: {simulate(matrix, occupied_visibles, 5)}")
