from copy import copy


def read_input():
    """Reads the input of the problem and returns it as a sorted numbers list"""
    numbers = []
    with open('solutions/day10/input.txt') as f:
        for line in f:
            numbers.append(int(line.strip(' \n')))
    return sorted(numbers)


def chain_all_adapters(numbers):
    """ Create a chain of all adapters starting at 0 end ending at the max value. 
        When multiple possibilities are present, pick the minimum.
        Returns the product of the amount of 1-jolts and 3-jolts. """
    numbers = copy(numbers)
    jolt_counts = dict.fromkeys(range(0, 4), 0)
    cur_jolt = 0
    while len(numbers) > 0:
        new_jolt = min(filter(lambda n: n - cur_jolt <= 3, numbers))
        jolt_counts[new_jolt - cur_jolt] += 1
        cur_jolt = new_jolt
        numbers.remove(cur_jolt)
    return(jolt_counts[1] * jolt_counts[3])


def distinct_chains(numbers):
    """ Calculate all distinct chains using Dynamic Programming.
        Use a dictionary to keep track of intermediate results. """
    dp_hist = dict.fromkeys(numbers, 0)
    dp_hist[max(numbers)] = 1
    for n in list(reversed(numbers)):
        for i in range(1, 4):
            if n - i in numbers:
                dp_hist[n-i] = dp_hist[n-i] + dp_hist[n]
    return dp_hist[0]


# Find the solutions for part 1 and 2 of the puzzle.
if __name__ == "__main__":
    numbers = read_input()
    numbers.insert(0, 0)
    numbers.append(max(numbers)+3)
    # Part 1
    print(
        f"(1-jolts * 3-jolts) for part 1 equals: {chain_all_adapters(numbers)}")
    # Part 2 dynamic programming
    print(
        f"The amount of distinct chains is equal to {distinct_chains(numbers)}")
