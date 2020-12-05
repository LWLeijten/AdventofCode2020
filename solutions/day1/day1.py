import itertools
from functools import reduce


def read_input():
    """Reads the input of the problem and returns it as a numbers list"""
    numbers = []
    with open('solutions/day1/input.txt') as f:
        for line in f:
            numbers.append(int(line.strip(' \n')))
    return numbers


def find_solution(numbers: [int], item_count: int):
    """ Iterate over all combinations of count 'item_count'
    until a solution has been found. Returns the product of the found combination.
    """
    for items in itertools.combinations(numbers, item_count):
        if sum(items) == 2020:
            result = reduce((lambda x, y: x * y), items)
            return result


# Find the solutions for part 1 and 2 of the puzzle.
if __name__ == "__main__":
    numbers = read_input()
    print(find_solution(numbers, 2))
    print(find_solution(numbers, 3))
