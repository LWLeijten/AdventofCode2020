import math

ROWS = 127
COLS = 7


def read_input():
    """Reads the input of the problem and returns it as a list of split instructions"""
    splits = []
    with open('solutions/day5/input.txt') as f:
        for line in f:
            splits.append(line.strip(' \n'))
    return splits


def bsp(splits, min_val, max_val):
    """ BSP algorithm to find the correct row and column
        as given by the split instructions in the input file."""
    if not splits and min_val == max_val:
        return min_val
    if splits[0] in ['F', 'L']:
        return bsp(splits[1:], min_val, math.floor((min_val + max_val)/2))
    elif splits[0] in ['B', 'R']:
        return bsp(splits[1:], math.ceil((min_val + max_val)/2), max_val)


def seat_id(row, col):
    """ Calculates the seat_id from given row and col."""
    return row * 8 + col


def missing_seat_ids(taken_seats):
    """ Finds all seat ids that should be present
        but are not yet taken by a boarding pass."""
    all_seats = set(range(min(taken_seats), max(taken_seats) + 1))
    return(set(taken_seats).symmetric_difference(all_seats))


# Find the solutions for part 1 and 2 of the puzzle.
if __name__ == "__main__":
    splits = read_input()
    seat_ids = list(map(lambda s: seat_id(bsp(s[:-3], 0, ROWS), bsp(s[-3:], 0, COLS)), splits)) # Oneliner more for fun than readability
    # Part 1
    print(max(seat_ids))
    # Part 2
    print(missing_seat_ids(seat_ids))
