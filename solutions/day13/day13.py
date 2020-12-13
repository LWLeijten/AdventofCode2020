import math
from functools import reduce


def read_input():
    """Read input and return our arrival time and a list of bus ids."""
    with open('solutions/day13/input.txt') as f:
        arrival = int(f.readline().strip())
        buses = f.readline().strip().split(',')
    return arrival, buses


def find_closest_bus(arrival, buses):
    """ Finds the time and id of the bus arriving soonest after our arrival.
        Returns the minutes we have to wait times the id of the bus. """
    buses = list(map(int, filter(lambda b: b != 'x', buses)))
    arrivals = list(map(lambda b: (b, math.ceil(arrival/b)*b), buses))
    bus, time = min(arrivals, key=lambda t: t[1])
    return (time - arrival) * bus


def chinese_remainder_theorem(nums, rems):
    """ Solves part two using the chinese remainder theorem.
        Finds the first moment in time for which all the buses arrive 
        after each other with deltas of the index in the original list. 
        See: (https://en.wikipedia.org/wiki/Chinese_remainder_theorem)"""
    prod = reduce((lambda x, y: x*y), nums)
    pp = list(map(lambda n: prod // n, nums))
    invs = [pow(p, -1, nums[i]) for i, p in enumerate(pp)]
    result = sum(rems[i]*pp[i]*invs[i] for i in range(len(nums))) % prod
    return result


# Find the solutions for part 1 and 2 of the puzzle.
if __name__ == "__main__":
    arrival, buses = read_input()
    # Part 1
    print(find_closest_bus(arrival, buses))
    # Part 2
    nums = list(map(lambda b: int(b), (filter(lambda b: b != 'x', buses))))
    rems = list(map(lambda n: n - buses.index(str(n)), nums))
    print(chinese_remainder_theorem(nums, rems))
